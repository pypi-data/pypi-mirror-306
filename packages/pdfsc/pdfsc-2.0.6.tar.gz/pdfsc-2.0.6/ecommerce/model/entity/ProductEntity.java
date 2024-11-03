package com.kiatkoding.ecommerce.model.entity;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Table(name = "product")
@Entity
@Data
@NoArgsConstructor
@AllArgsConstructor
public class ProductEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    public Integer id;

    @Column(nullable = false)
    public String name;

    @Column(nullable = false)
    public String image;

    @Column(nullable = false)
    public Double price;

    @Column(nullable = true)
    public Double rating;

    @Column(nullable = false)
    public String description;

    @ManyToOne(fetch = FetchType.EAGER)
    @JoinColumn(name = "category_id", nullable = false)
    public CategoryEntity category;
}
