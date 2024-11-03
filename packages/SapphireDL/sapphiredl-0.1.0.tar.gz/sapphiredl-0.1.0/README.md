# Описание библиотеки глубокого обучения Sapphire

## Введение
Эта документация посвящена библиотеке глубокого обучения, разработанной для эффективного создания и обучаения
моделей машинного обучения

## Установка
Для установки библиотеки выполните следующую команду:
```bash
pip install sapphirepy
```

## Основные возможности
Пример для XOR

### 1. Создание модели
Библиотека позволяет легко создавать сложные нейронные сети с использованием высокоуровневых API.

```python
import numpy as np

from training import train
from neural_networks import NeuralNetwork
from layers import LinearLayer, HypTan

inputs = np.array([
    [0, 0],
    [1, 0],
    [0, 1],
    [1, 1]
])

targets = np.array([
    [1, 0],
    [0, 1],
    [0, 1],
    [1, 0]
])

nn = NeuralNetwork([
    LinearLayer(input_size=2, output_size=2),
    HypTan(),
    LinearLayer(input_size=2, output_size=2)
])
```

### 2. Обучение модели
Обучение моделей становится простым с помощью встроенных методов.

```python
num_epochs = 5000

train(neural_network=nn, inputs=inputs, targets=targets, epochs_count=num_epochs)
```

### 3. Прогнозирование
После обучения можно использовать модель для прогнозирования новых данных.

```python
for x, y in zip(inputs, targets):
    predicted = nn.forward(x)
    print(x, predicted, y)  # np.round(predicted, decimals=7)
```

## Документация по API

Для более подробной информации о каждом методе и классе библиотеки, пожалуйста, обратитесь к документации API.

## Дополнительные ресурсы

- [Документация](https://github.com/itbert/SapphireDL/documentation)
- [Примеры использования](https://github.com/itbert/SapphireDL)
