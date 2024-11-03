package com.kiatkoding.ecommerce.repository;

import com.kiatkoding.ecommerce.model.entity.UserEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface UserRepository extends JpaRepository<UserEntity, Integer> {

    Optional<UserEntity> findByPhoneNumber(String phoneNumber);
}
