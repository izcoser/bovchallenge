# Desafio BovControl

Esse repositório é implementação do [desafio backend](https://github.com/bovcontrol/milk-hiring/blob/master/backend.md) da BovControl. Para a solução, foi escolhida a linguagem Python com o Django Rest Framework.

# Instruções

Para instalar e rodar localmente:

```
git clone https://izcoser/bovchallenge
cd bovchallenge
pip install -r requirements.txt
python manage.py runserver
```

# Informações de implementação

Usando o Django Rest Framework, foram criados 4 models: Cost, Farm, Farmer e MilkDeliveries. Eles guardam, respectivamente, dados dos custos em cada semestre do ano, de fazenda, de fazendeiros e de entregas de leite. As fazendas têm chave estrangeira para fazendeiro e as entregas têm chave estrangeira para fazenda.

O repositório já consta com o arquivo db.sqlite3 com as tabelas criadas e com dados de custos semestrais preenchidos, entre outros.

Os endpoints são: 

```
costs/
farmers/
farms/
deliveries/
farmer_output/<str:farmer_code>/<int:month>/<int:year>
farmer_monthly_price/<str:farmer_code>/<int:month>/<int:year>
farmer_yearly_price/<str:farmer_code>/<int:year>
```

# Exemplos de uso

## GET

```
http http://127.0.0.1:8000/costs/

[
    {
        "base": "1.800",
        "bonus": "0.000",
        "id": 1,
        "over_50": "0.060",
        "semester": 1,
        "under_50": "0.050"
    },
    {
        "base": "1.950",
        "bonus": "0.010",
        "id": 2,
        "over_50": "0.000",
        "semester": 2,
        "under_50": "0.000"
    }
]
```

```
http http://127.0.0.1:8000/deliveries/
[
    {
        "amount": "50.000",
        "date": "2022-08-25T00:00:00Z",
        "farm": 1,
        "id": 1
    }
]
```

## POST

```
http --json POST http://127.0.0.1:8000/farmers/ name="João Carlos" code="jcarlos1" cnpj="13245"

{
    "cnpj": "13245",
    "code": "jcarlos1",
    "id": 4,
    "name": "João Carlos"
}
```


```
http --json POST http://127.0.0.1:8000/farms/ name="Fazenda do João Carlos" code="jcarlos1f" distance=500 owner=4

{
    "code": "jcarlos1f",
    "distance": "500.000",
    "id": 3,
    "name": "Fazenda do João Carlos",
    "owner": 4
}

```



```
http --json POST http://127.0.0.1:8000/deliveries/ amount=150 date="2022-08-28" farm=1

{
    "amount": "150.000",
    "date": "2022-08-28T00:00:00Z",
    "farm": 1,
    "id": 11
}

```
