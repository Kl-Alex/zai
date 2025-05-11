def generate_key(modulus=256):
    """
    Генерация простого ключа (в реальном FHE используется сложная математика).
    Здесь ключ — это случайное число, используемое для шифрования.
    """
    import random
    key = random.randint(1, modulus - 1)
    return key


def encrypt(plaintext, key, modulus=256):
    """
    Шифрование: добавляем ключ к открытому тексту по модулю.
    """
    return (plaintext + key) % modulus


def decrypt(ciphertext, key, modulus=256):
    """
    Расшифровка: вычитаем ключ из шифротекста по модулю.
    """
    return (ciphertext - key) % modulus


def homomorphic_add(c1, c2, modulus=256):
    """
    Гомоморфное сложение двух зашифрованных чисел.
    """
    return (c1 + c2) % modulus


# Пример использования
if __name__ == "__main__":
    # Генерация ключа
    key = generate_key()

    # Открытые данные
    a = int(input('Введите а: '))
    b = int(input('Введите б: '))

    # Шифрование
    c_a = encrypt(a, key)
    c_b = encrypt(b, key)

    print(f"Зашифрованное a: {c_a}")
    print(f"Зашифрованное b: {c_b}")

    # Гомоморфное сложение
    c_sum = homomorphic_add(c_a, c_b)
    print(f"Зашифрованная сумма: {c_sum}")

    # Расшифровка результата
    result = decrypt(c_sum, key)
    print(f"Результат расшифровки: {result}")
    print(f"Ожидаемый результат (a + b): {a + b}")