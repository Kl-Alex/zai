import tenseal as ts
import numpy as np

# 1. Настройка параметров FHE
def setup_fhe():
    # Создаём контекст FHE (схема CKKS)
    context = ts.context(ts.SCHEME_TYPE.CKKS, poly_modulus_degree=8192, coeff_mod_bit_sizes=[60, 40, 40, 60])
    context.global_scale = 2**40  # Масштаб для дробных чисел
    context.generate_galois_keys()  # Ключи для умножения и поворотов
    return context

# 2. Определение простой нейросети
class SimpleEncryptedNN:
    def __init__(self, context):
        self.context = context
        # Веса модели (обученные заранее)
        self.weights1 = np.random.randn(2, 3)  # Входной слой -> скрытый
        self.bias1 = np.random.randn(3)
        self.weights2 = np.random.randn(3, 1)  # Скрытый -> выходной
        self.bias2 = np.random.randn(1)

    def forward(self, x_enc):
        # Первый слой: линейная комбинация + ReLU
        x_enc = x_enc.mm(self.weights1) + self.bias1
        x_enc = x_enc.polyval([0, 1])  # Аппроксимация ReLU (линейная функция)

        # Второй слой: линейная комбинация
        x_enc = x_enc.mm(self.weights2) + self.bias2
        return x_enc

# 3. Пример использования
if __name__ == "__main__":
    # Настройка FHE
    context = setup_fhe()

    # Создание нейросети
    model = SimpleEncryptedNN(context)

    # Входные данные (зашифрованные)
    input_data = np.array([1.5, -0.5])
    input_enc = ts.ckks_vector(context, input_data)

    # Предсказание на зашифрованных данных
    output_enc = model.forward(input_enc)

    # Расшифровка результата
    output = output_enc.decrypt()[0]
    print("Результат предсказания (расшифрованный):", output)