package com.kiatkoding.ecommerce.repository;

import com.kiatkoding.ecommerce.model.entity.ProductEntity;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

@Repository
public interface ProductRepository extends JpaRepository<ProductEntity, Integer> {


    Page<ProductEntity> findAll(Pageable pageable);

    // naming method
    Page<ProductEntity> findByNameContainsIgnoreCaseAndDescriptionContainsIgnoreCase(String name, String description, Pageable pageable);

    // query method
    @Query("""
            SELECT product FROM ProductEntity product WHERE
            LOWER(product.name) LIKE LOWER(CONCAT('%', :query, '%')) OR
            LOWER(product.description) LIKE LOWER(CONCAT('%', :query, '%'))
            """)
    Page<ProductEntity> filter(String query, Pageable pageable);

    @Query("""
            SELECT product FROM ProductEntity product WHERE
            (LOWER(product.name) LIKE LOWER(CONCAT('%', :query, '%')) OR
            LOWER(product.description) LIKE LOWER(CONCAT('%', :query, '%'))) AND
            product.category.id = :categoryId
            """)
    Page<ProductEntity> filter(String query, Integer categoryId, Pageable pageable);

    @Query("""
            SELECT product FROM ProductEntity product WHERE
            product.category.id = :categoryId
            """)
    Page<ProductEntity> filter(Integer categoryId, Pageable pageable);
}
