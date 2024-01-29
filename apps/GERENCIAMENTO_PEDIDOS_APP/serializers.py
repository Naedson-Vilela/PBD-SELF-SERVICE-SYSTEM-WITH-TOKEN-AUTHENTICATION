from rest_framework import serializers
from .models import *


class MesaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Mesa
        fields = (
            '__all__'
        )


class CategoriaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categoria
        fields = '__all__'


class ProdutoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Produto
        fields = '__all__'


class ProdutoQuantidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProdutoQuantidade
        fields = '__all__'

    @staticmethod
    def __validate_produto_quantidade(quantidade):
        serializers = [ProdutoQuantidadeSerializer(item) for item in quantidade]
        validade = [item.is_valid() for item in serializers]
        validate = True if all(validade) else False
        return validate

    @staticmethod
    def update_many_produto_quantidade(produto_quantide, produto_quantidade_data):
        serializers = [[item, data] for item, data in zip(produto_quantide, produto_quantidade_data)]
        produto_quantidade_serializers = []
        for item in serializers:
            produto_quantidade_serializers.append(ProdutoQuantidadeSerializer(item[0], data=item[1], partial=True))

        validate = [item.is_valid() for item in produto_quantidade_serializers]
        if all(validate):
            for item in produto_quantidade_serializers:
                item.save()
            return validate, [item[1] for item in serializers]
        return validate, []

class PedidoSerializer(serializers.ModelSerializer):

    produtos_quantidades = ProdutoQuantidadeSerializer(many=True, read_only=True)

    class Meta:
        model = Pedido
        fields = '__all__'

    @staticmethod
    def criar_pedido_produtos_quantidades(pedido, produto_quantidade):
        pedido['mesa_id'] = Mesa.objects.get(pk=pedido.get('mesa_id'))
        pedido_object = Pedido.objects.create(**pedido)
        for item in produto_quantidade:
            item['produto_id'] = Produto.objects.get(pk=item.get('produto_id'))
        pedidos_quantides = [ProdutoQuantidade.objects.create(**item) for item in produto_quantidade]
        pedido_object.produtos_quantidades.set(pedidos_quantides)
        return PedidoSerializer(pedido, read_only=True)