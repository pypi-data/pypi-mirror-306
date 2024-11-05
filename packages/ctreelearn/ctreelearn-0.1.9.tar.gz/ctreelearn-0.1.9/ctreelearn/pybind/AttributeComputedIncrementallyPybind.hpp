#ifndef ATTRIBUTE_COMPUTED_INCREMENTALLY_PYBIND_H
#define ATTRIBUTE_COMPUTED_INCREMENTALLY_PYBIND_H


#include "../include/AttributeComputedIncrementally.hpp"
#include "../include/NodeCT.hpp"

#include "../pybind/ComponentTreePybind.hpp"

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>
#include <algorithm> 
#include <cmath>
#include <iostream>
#include <torch/extension.h>

class AttributeComputedIncrementallyPybind : public AttributeComputedIncrementally{

    public:
    using AttributeComputedIncrementally::AttributeComputedIncrementally;


	static py::array_t<float> computerArea(ComponentTreePybind *tree){
		const int n = tree->getNumNodes();
		float *attrs = new float[n];
		AttributeComputedIncrementally::computerAttribute(tree->getRoot(),
			[&attrs](NodeCT* node) -> void { //pre-processing
				attrs[node->getIndex()] = node->getCNPs().size(); //area
			},
			[&attrs](NodeCT* parent, NodeCT* child) -> void { //merge-processing
				attrs[parent->getIndex()] += attrs[child->getIndex()];
			},
			[](NodeCT* node) -> void { //post-processing			
		});
	    py::array_t<float> numpy = py::array(py::buffer_info(
			attrs,            
			sizeof(float),     
			py::format_descriptor<float>::value, 
			1,         
			{  n }, 
			{ sizeof(float) }
	    ));
		return numpy;
	}

    static std::pair<py::dict, py::array_t<float>> computerBasicAttributes(ComponentTreePybind *tree){
        
		auto [attributeNames, ptrValues] = AttributeComputedIncrementally::computerBasicAttributes(tree);
		const int numAttribute = attributeNames.NUM_ATTRIBUTES;
		const int n = tree->getNumNodes();
        
		
		std::vector<std::string> keys;
		std::vector<int> values;

		// 1. Copiar chaves e valores para vetores separados
		for (const auto& pair : attributeNames.mapIndexes) {
			keys.push_back(pair.first);
			values.push_back(pair.second);
		}

		// 2. Criar um vetor de índices para ordenar os valores
		std::vector<size_t> indices(values.size());
		std::iota(indices.begin(), indices.end(), 0);
		std::sort(indices.begin(), indices.end(), [&values](size_t i1, size_t i2) { return values[i1] < values[i2]; });

		py::dict dict;
		for (size_t i = 0; i < indices.size(); ++i) {
			dict[py::str( keys[indices[i]] )] = values[indices[i]] / n; 
		}

	    py::array_t<float> numpy = py::array(py::buffer_info(
			ptrValues,            
			sizeof(float),     
			py::format_descriptor<float>::value, 
			2,         
			{  n,  numAttribute }, 
			{ sizeof(float), sizeof(float) * n }
	    ));
		
		return std::make_pair(dict, numpy);
	}


	static torch::Tensor computerJacobian(ComponentTreePybind *tree) {
        // Crie a matriz J no C++
        torch::Tensor J = torch::zeros({tree->getNumNodes(), tree->getRoot()->getAreaCC()}, torch::kFloat);

        // Aplique o processamento incremental usando as funções de callback
        AttributeComputedIncrementally::computerAttribute(tree->getRoot(),
			[&J](NodeCT* node) -> void { //pre-processing
				for(int pixel: node->getCNPs())
					J[node->getIndex()][pixel] = 1;
			},
			[&J](NodeCT* parent, NodeCT* child) -> void { //merge-processing
				for(int pixel: child->getCNPs())
					J[parent->getIndex()][pixel] = 1;
			},
			[](NodeCT* node) -> void { //post-processing			
		});

        // Retorne a matriz J como um tensor PyTorch
        return J;
    }
};

#endif 