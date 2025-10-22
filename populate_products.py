#!/usr/bin/env python
"""
Script para popular o banco de dados com produtos de exemplo
Execute: python populate_products.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatbot.settings')
django.setup()

from core.models import Product

def populate():
    products = [
        {
            'name': 'Ração Royal Canin Golden Retriever Adult',
            'category': 'racao',
            'price': 289.90,
            'stock': 15,
            'description': 'Ração premium especialmente formulada para Golden Retriever adultos. Rica em ômega 3 e 6 para pelagem brilhante.',
            'target_species': 'cachorro',
            'target_breed': 'Golden Retriever',
            'target_age': 'adulto',
            'is_available': True
        },
        {
            'name': 'Ração Premier Pet Golden Filhote',
            'category': 'racao',
            'price': 199.90,
            'stock': 8,
            'description': 'Ração para filhotes de raças grandes. Desenvolvida com DHA e EPA para desenvolvimento cognitivo.',
            'target_species': 'cachorro',
            'target_breed': 'Golden Retriever',
            'target_age': 'filhote',
            'is_available': True
        },
        {
            'name': 'Ração Pedigree Raças Pequenas',
            'category': 'racao',
            'price': 89.90,
            'stock': 25,
            'description': 'Ração econômica para cães de raças pequenas. Nutrição completa e balanceada.',
            'target_species': 'cachorro',
            'target_breed': '',
            'target_age': 'adulto',
            'is_available': True
        },
        {
            'name': 'Ração Royal Canin Persian Adult',
            'category': 'racao',
            'price': 189.90,
            'stock': 12,
            'description': 'Ração específica para gatos da raça Persa. Formato exclusivo da croquete facilita a preensão.',
            'target_species': 'gato',
            'target_breed': 'Persa',
            'target_age': 'adulto',
            'is_available': True
        },
        {
            'name': 'Ração Whiskas Gatos Adultos Carne',
            'category': 'racao',
            'price': 69.90,
            'stock': 30,
            'description': 'Ração para gatos adultos sabor carne. Nutrição balanceada com vitaminas e minerais.',
            'target_species': 'gato',
            'target_breed': '',
            'target_age': 'adulto',
            'is_available': True
        },
        {
            'name': 'Petisco DreamBone Mini para Cães',
            'category': 'petisco',
            'price': 29.90,
            'stock': 50,
            'description': 'Ossinhos mastigáveis sem couro. Rico em vitaminas e minerais. Tamanho mini para raças pequenas.',
            'target_species': 'cachorro',
            'target_breed': '',
            'target_age': 'todos',
            'is_available': True
        },
        {
            'name': 'Brinquedo Kong Classic',
            'category': 'brinquedo',
            'price': 79.90,
            'stock': 20,
            'description': 'Brinquedo resistente de borracha natural. Ideal para rechear com petiscos e mantém o cão entretido.',
            'target_species': 'cachorro',
            'target_breed': '',
            'target_age': 'todos',
            'is_available': True
        },
        {
            'name': 'Arranhador para Gatos Torre 3 Andares',
            'category': 'brinquedo',
            'price': 249.90,
            'stock': 5,
            'description': 'Torre com 3 andares, arranhadores de sisal e tocas. Mantém o gato ativo e preserva seus móveis.',
            'target_species': 'gato',
            'target_breed': '',
            'target_age': 'todos',
            'is_available': True
        },
        {
            'name': 'Coleira Peitoral Acolchoada Tam G',
            'category': 'acessorio',
            'price': 59.90,
            'stock': 18,
            'description': 'Peitoral acolchoado para cães de porte grande. Distribui pressão uniformemente. Ajustável.',
            'target_species': 'cachorro',
            'target_breed': '',
            'target_age': 'todos',
            'is_available': True
        },
        {
            'name': 'Shampoo Neutro para Cães e Gatos',
            'category': 'higiene',
            'price': 24.90,
            'stock': 40,
            'description': 'Shampoo pH neutro para uso frequente. Fórmula suave que não agride a pele. 500ml.',
            'target_species': 'todos',
            'target_breed': '',
            'target_age': 'todos',
            'is_available': True
        },
        {
            'name': 'Antipulgas Bravecto para Cães 20-40kg',
            'category': 'saude',
            'price': 189.90,
            'stock': 0,  # SEM ESTOQUE
            'description': 'Proteção contra pulgas e carrapatos por 12 semanas. Comprimido palatável.',
            'target_species': 'cachorro',
            'target_breed': '',
            'target_age': 'adulto',
            'is_available': False  # INDISPONÍVEL
        },
        {
            'name': 'Ração Sênior Royal Canin Medium Ageing 10+',
            'category': 'racao',
            'price': 239.90,
            'stock': 10,
            'description': 'Ração para cães idosos de raças médias (10+ anos). Fórmula com antioxidantes e suporte articular.',
            'target_species': 'cachorro',
            'target_breed': '',
            'target_age': 'idoso',
            'is_available': True
        },
    ]
    
    created_count = 0
    for product_data in products:
        product, created = Product.objects.get_or_create(
            name=product_data['name'],
            defaults=product_data
        )
        if created:
            created_count += 1
            print(f"✅ Criado: {product.name} - R$ {product.price}")
        else:
            print(f"ℹ️  Já existe: {product.name}")
    
    print(f"\n🎉 Total de produtos criados: {created_count}")
    print(f"📊 Total de produtos no banco: {Product.objects.count()}")
    print(f"✅ Produtos disponíveis: {Product.objects.filter(is_available=True, stock__gt=0).count()}")

if __name__ == '__main__':
    populate()
