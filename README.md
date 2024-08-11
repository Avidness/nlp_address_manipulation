# nlp_address_manipulation

Includes source code for fine-tuning a pretrained transformer model to insert spaces into addresses that are missing them. E.g.,

```
123NEWYORKNY10023 -> 123 NEW YORK NY 10023
```

Additionally - Given the data below, train a Logicistic Regression Model to classify countries usign TF-IDF Vectors of the address.

| address | country |
|-----------------|-----------------|
| 123 NEW YORK NY 10023 | US |
| 455492 MOSCOW | RU |
| KOWLOON, HK | CN |

If you're pulling data from OS, add `config.ini` with the following params:
```
[opensearch]
host = localhost
port = 9200
user = admin
pw = admin
```