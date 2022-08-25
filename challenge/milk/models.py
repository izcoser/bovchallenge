from django.db import models

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)

    class Meta:
        abstract = True

class BaseCost(models.Model):
    # Usando DecimalField porque vamos lidar com cálculos monetários e Float possui problemas de precisão.
    
    # Preço base por litro.
    base = models.DecimalField(max_digits=8, decimal_places=3)
    
    # Custo por km até 50km.
    under_50 = models.DecimalField(max_digits=6, decimal_places=3)
    
    # Custo por km acima de 50km.
    over_50 = models.DecimalField(max_digits=6, decimal_places=3)
    
    # Bônus p/ produção acima de 10.000 L, por litro.
    bonus = models.DecimalField(max_digits=6, decimal_places=3)

    class Meta:
        abstract = True

class Farmer(BaseModel):
    code = models.CharField(max_length=10)
    cnpj = models.CharField(max_length=18)

class Farm(BaseModel):
    # Distância até a fábrica, em km.
    # 8 dígitos (3 casas decimais) são suficientes para cobrir qualquer distância em km entre dois pontos no planeta,
    # com precisão até o último metro.
    distance = models.DecimalField(max_digits=8, decimal_places=3)
    code = models.CharField(max_length=10)
    owner = models.OneToOneField(Farmer, on_delete=models.CASCADE, primary_key=True)

# Custos do primeiro semestre.
class CostFirst(BaseCost):
    pass

# Custos do segundo semestre.
class CostSecond(BaseCost):
    pass

class MilkDeliveries(models.Model):
    farm = models.OneToOneField(Farm, on_delete=models.CASCADE, primary_key=True)
    # Quantidade entregue, em litros, com precisão de mililitro.
    amount = models.DecimalField(max_digits=15, decimal_places=3)
    date = models.DateTimeField()