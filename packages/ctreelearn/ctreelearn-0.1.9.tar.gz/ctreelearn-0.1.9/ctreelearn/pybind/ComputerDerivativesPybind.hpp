
#include "../pybind/ComponentTreePybind.hpp"
#include "../pybind/ResidualTreePybind.hpp"
#include "../include/NodeCT.hpp"
#include "../include/NodeRes.hpp"
#include "../include/AttributeComputedIncrementally.hpp"

#include <vector>
#include <stack>
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

       
    static py::tuple gradientsResidualTree(ResidualTreePybind* residualTree, torch::Tensor attrs, torch::Tensor sigmoid, torch::Tensor gradientOfLoss) {
        float* attributes = attrs.data_ptr<float>(); 
        float* sigmoid_ptr = sigmoid.data_ptr<float>();
        float* gradLoss = gradientOfLoss.data_ptr<float>();

        int rows = attrs.size(0);
        int cols = attrs.size(1);
        torch::Tensor gradFilterWeights = torch::empty({rows * cols}, torch::kFloat32);
        torch::Tensor gradFilterBias = torch::empty({rows}, torch::kFloat32);

        float* gradFilterWeights_ptr = gradFilterWeights.data_ptr<float>();
        float* gradFilterBias_ptr = gradFilterBias.data_ptr<float>();

        int* restOfImage = residualTree->getRestOfImage();
        ComponentTree *tree = residualTree->getCTree();
        int residuePos=0;
        int residueNeg=0;
        int residue;
        for(NodeCT* node: tree->getListNodes()){
            int id = node->getIndex();
            
            //computer residue
            if(id > 0){
                 if(node->isMaxtreeNode()){
                    residuePos += node->getParent()->getResidue();
                }else{
                    residueNeg -= node->getParent()->getResidue();
                }
            }
            if(node->isMaxtreeNode())
                residue = restOfImage[node->getRep()] + residuePos;
            else
                residue = restOfImage[node->getRep()] - residueNeg;
            
            //computer gradients
            float dSigmoid = sigmoid_ptr[id] * (1 - sigmoid_ptr[id]);
            gradFilterBias_ptr[id] = residue * dSigmoid;
            for (int j = 0; j < cols; j++){
                gradFilterWeights_ptr[id * cols + j] = residue * dSigmoid * attributes[j * rows + id];
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

        int residuePos=tree->getRoot()->getLevel();
        int residueNeg=tree->getRoot()->getLevel();
        int residue;
        for(NodeCT* node: tree->getListNodes()){
            int id = node->getIndex();
            
            //computer residue
            if(id > 0){
                 if(node->isMaxtreeNode()){
                    residuePos += node->getParent()->getResidue();
                }else{
                    residueNeg -= node->getParent()->getResidue();
                }
            }
            if(node->isMaxtreeNode())
                residue = residuePos;
            else
                residue = residueNeg;
            
            //computer gradients
            float dSigmoid = sigmoid_ptr[id] * (1 - sigmoid_ptr[id]);
            gradFilterBias_ptr[id] = residue * dSigmoid;
            for (int j = 0; j < cols; j++){
                gradFilterWeights_ptr[id * cols + j] = residue * dSigmoid * attributes[j * rows + id];
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