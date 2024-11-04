
#include "../pybind/ComponentTreePybind.hpp"
#include "../include/NodeCT.hpp"
#include "../include/AttributeComputedIncrementally.hpp"

#include <vector>
#include <tuple>
#include <pybind11/pybind11.h>
#include <torch/extension.h>

#include <iostream>

namespace py = pybind11;

#ifndef COMPUTER_DERIVATIVE_PYBIND_H
#define COMPUTER_DERIVATIVE_PYBIND_H


class ComputerDerivativesPybind {
    
    private:
        

    public:
        
       static py::tuple gradients_numpy(ComponentTreePybind* tree, py::array_t<float> &attrs, std::vector<float> sigmoid, py::array_t<float> gradientOfLoss) {
            auto buf_attrs = attrs.request();
            float* attributes = (float *) buf_attrs.ptr;
            int rows = buf_attrs.shape[0];
            int cols = buf_attrs.shape[1];
            
            float *dWeight = new float[rows * cols];
            float *dBias = new float[rows];
            for(NodeCT* node: tree->getListNodes()){
                int id = node->getIndex();
                dBias[id] = (sigmoid[id] * (1 - sigmoid[id])) * node->getResidue();
                for (int j = 0; j < cols; j++)
                    dWeight[id + (rows * j)] = (sigmoid[id] * (1 - sigmoid[id])) * attributes[id + (rows * j)] * node->getResidue();

                if (id > 0) {
                    int idParent = node->getParent()->getIndex();
                    dBias[id] += dBias[idParent];
                    for (int j = 0; j < cols; j++)
                        dWeight[id + (rows * j)] += dWeight[idParent + rows * j];
                }
            }


            auto buf_gradLoss = gradientOfLoss.request();
            float* gradLoss = (float *) buf_gradLoss.ptr;
            
            float *gradWeight = new float[cols];
            float *gradBias = new float[1];
            gradBias[0] = 0;
            for (int j = 0; j < cols; j++)
                gradWeight[j] = 0;
            

            float *summationGrad = new float[tree->getNumNodes()];
            float *gradInput = new float[tree->getNumRowsOfImage() * tree->getNumColsOfImage()];
            AttributeComputedIncrementally::computerAttribute(tree->getRoot(),
                    [&summationGrad, &gradLoss, &sigmoid](NodeCT* node) -> void { //pre-processing
                        summationGrad[node->getIndex()] = 0;
                        for(int p: node->getCNPs()){
                            summationGrad[node->getIndex()] += gradLoss[p];
                        }
                        summationGrad[node->getIndex()] = summationGrad[node->getIndex()] * sigmoid[node->getIndex()]; 
                    },
                    [&summationGrad](NodeCT* parent, NodeCT* child) -> void { //merge-processing
                        summationGrad[parent->getIndex()] += summationGrad[child->getIndex()];
                    },
                    [&summationGrad, &gradInput, &gradWeight,&gradBias, &dBias, &dWeight, &rows, &cols, &gradLoss ](NodeCT* node) -> void { //post-processing	
                        for(int p: node->getCNPs()){
                            gradInput[p] = summationGrad[node->getIndex()]; 
                            gradBias[0] += gradLoss[p] * dBias[node->getIndex()];
                            for (int j = 0; j < cols; j++)
                                gradWeight[j] += gradLoss[p] * dWeight[node->getIndex() + (rows * j)];
                            }		
                    }
            );
            
            
            delete[] summationGrad;
            py::array_t<float> gradWeight_np = py::array(py::buffer_info(
                    gradWeight,            
                    sizeof(float),     
                    py::format_descriptor<float>::value, 
                    1,         
                    {  cols }, 
                    { sizeof(float) }
            ));

            py::array_t<float> gradBias_np = py::array(py::buffer_info(
                    gradBias,            
                    sizeof(float),     
                    py::format_descriptor<float>::value, 
                    1,         
                    {  1 }, 
                    { sizeof(float) }
            ));

            py::array_t<float> gradInput_np = py::array(py::buffer_info(
                    gradInput,            
                    sizeof(float),     
                    py::format_descriptor<float>::value, 
                    1,         
                    {  tree->getNumRowsOfImage() * tree->getNumColsOfImage() }, 
                    { sizeof(float) }
            ));


            return py::make_tuple(gradWeight_np, gradBias_np, gradInput_np);
        }
        
    static py::tuple gradients(ComponentTreePybind* tree, torch::Tensor attrs, torch::Tensor sigmoid, torch::Tensor gradientOfLoss) {
        float* attributes = attrs.data_ptr<float>(); 
        float* sigmoid_ptr = sigmoid.data_ptr<float>();
        float* gradLoss = gradientOfLoss.data_ptr<float>();

        int rows = attrs.size(0);
        int cols = attrs.size(1);
        torch::Tensor gradFilterWeights = torch::empty({rows * cols}, torch::kFloat32);
        torch::Tensor gradFilterBias = torch::empty({rows}, torch::kFloat32);

        float* gradFilterWeights_ptr = gradFilterWeights.data_ptr<float>();
        float* gradFilterBias_ptr = gradFilterBias.data_ptr<float>();

        for (NodeCT* node : tree->getListNodes()) {
            int id = node->getIndex();
            gradFilterBias_ptr[id] = (sigmoid_ptr[id] * (1 - sigmoid_ptr[id])) * node->getLevel();
            for (int j = 0; j < cols; j++){
                gradFilterWeights_ptr[id * cols + j] = (sigmoid_ptr[id] * (1 - sigmoid_ptr[id])) *  attributes[j * rows + id] * node->getLevel(); //Pytorch: vetor "attributes" precisou ser acesso de forma transposta
            }
        }

        torch::Tensor gradWeight = torch::zeros({cols}, torch::kFloat32);
        torch::Tensor gradBias = torch::zeros({1}, torch::kFloat32);

        float* gradWeight_ptr = gradWeight.data_ptr<float>();
        float* gradBias_ptr = gradBias.data_ptr<float>();
        
        float* summationGrad_ptr = new float[tree->getNumNodes()];  
        AttributeComputedIncrementally::computerAttribute(tree->getRoot(),
            [&summationGrad_ptr, &gradLoss](NodeCT* node) -> void { // pre-processing
                summationGrad_ptr[node->getIndex()] = 0;
                for (int p : node->getCNPs()) {
                    summationGrad_ptr[node->getIndex()] += gradLoss[p];
                }
            },
            [&summationGrad_ptr](NodeCT* parent, NodeCT* child) -> void { // merge-processing
                summationGrad_ptr[parent->getIndex()] += summationGrad_ptr[child->getIndex()];
            },
            [&summationGrad_ptr, &gradWeight_ptr, &gradBias_ptr, &gradFilterBias_ptr, &gradFilterWeights_ptr, &cols](NodeCT* node) -> void { // post-processing
                gradBias_ptr[0] += summationGrad_ptr[node->getIndex()] * gradFilterBias_ptr[node->getIndex()];
                for (int j = 0; j < cols; j++)
                    gradWeight_ptr[j] += summationGrad_ptr[node->getIndex()] * gradFilterWeights_ptr[node->getIndex() * cols + j];
                
            }
        );
        delete[] summationGrad_ptr;
        return py::make_tuple(gradWeight, gradBias);
    }


};

#endif