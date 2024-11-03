package com.kiatkoding.ecommerce.service;

import com.kiatkoding.ecommerce.model.entity.ProductEntity;
import com.kiatkoding.ecommerce.model.response.PagingInfo;
import com.kiatkoding.ecommerce.repository.ProductRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class ProductService {

    private final ProductRepository productRepository;

    public PagingInfo<ProductEntity> getProducts(
            Integer pageNumber,
            Integer pageSize
    ) {
        PageRequest pageRequest = PageRequest.of(pageNumber-1, pageSize);
        Page<ProductEntity> products = productRepository.findAll(pageRequest);

        return PagingInfo.convertFromPage(products);
    }

    public PagingInfo<ProductEntity> getProducts(
            Integer pageNumber,
            Integer pageSize,
            String query
    ) {
        PageRequest pageRequest = PageRequest.of(pageNumber-1, pageSize);
        Page<ProductEntity> products = productRepository
                .filter(query, pageRequest);

        return PagingInfo.convertFromPage(products);
    }

    public PagingInfo<ProductEntity> getProducts(
            Integer pageNumber,
            Integer pageSize,
            String query,
            Integer categoryId
    ) {
        PageRequest pageRequest = PageRequest.of(pageNumber-1, pageSize);
        Page<ProductEntity> products = productRepository
                .filter(query, categoryId, pageRequest);

        return PagingInfo.convertFromPage(products);
    }

    public PagingInfo<ProductEntity> getProducts(
            Integer pageNumber,
            Integer pageSize,
            Integer categoryId
    ) {
        PageRequest pageRequest = PageRequest.of(pageNumber-1, pageSize);
        Page<ProductEntity> products = productRepository
                .filter(categoryId, pageRequest);

        return PagingInfo.convertFromPage(products);
    }
}
