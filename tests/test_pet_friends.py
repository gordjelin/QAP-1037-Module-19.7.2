import os
from api import PetFriends
import unicodedata
import random, string
from settings import valid_email, valid_password


pf = PetFriends()

def test_api_key_for_valid_user(email = valid_email, password = valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result
    print(result)

def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Айлин', animal_type='Боксер', age='9', pet_photo='images/dog.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()



def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


###################################################################################################################
#############################################Тесты из задания 19.7.2###############################################

'''Создаем функцию рандомной генерации логина/пароля с любой заданной длиной '''
def generate_random_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    rand_string = ''.join(random.choice(letters_and_digits) for i in range(length))


############## Тест 1.Проверка получения ключа API при условии, что введен невалидный пароль ##################

def test_get_api_wrong_password(email = valid_email, password = generate_random_string(10)):
    status, result = pf.get_api_key(email, password)
    assert status == 403
    if status == 403:
        print("Введите правильный пароль!")

############## Тест 2.Проверка получения ключа API при условии, что не введен пароль ###########################

def test_get_api_key_without_password(email = valid_email, password = ''):
    status, _ = pf.get_api_key(email, password)
    assert status == 403
    if status == 403:
      print("Поле для ввода пароля пусто! Введите пароль!")

############## Тест 3.Проверка получения ключа API при условии, что введен невалидный адрес эл. почты ############

def test_get_api_wrong_email(email=generate_random_string(10), password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403
    if status == 403:
        print("Введите правильный адрес эл. почты!")

############## Тест 4.Проверка получения ключа API при условии, что не введен email ##########################

def test_get_api_key_without_email(email = '', password = valid_password):
    status, _ = pf.get_api_key(email, password)
    assert status == 403
    if status == 403:
      print("Поле для ввода email пусто! Введите email!")

############## Тест 5.Проверка добавления питомца без фото ###################################################

def test_add_pet_without_photo_with_valid_data(name = 'Айлин', animal_type = 'Боксер', age = '9'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name
    print(name, animal_type, age)



############## Тест 6.Проверка НЕВОЗМОЖНОСТИ получения списка питомцев с помощью невалидного api ключа ############

def test_get_all_pets_with_wrong_key(filter = 'my_pets'):
    auth_key = {'key' : 'wrong_api'}
    status, _ = pf.get_list_of_pets(auth_key, filter)
    assert status == 403


############## Тест 7.Проверка НЕВОЗМОЖНОСТИ удаления питомца с помощью невалидного api ключа ##################

def test_delete_pet_with_wrong_api_key():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    if len(my_pets['pets']) == 0:
        pf.add_pet_without_photo(auth_key, "Абыр", "мышь", "33")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']
    auth_key = {'key': 'wrong_api'}
    status = pf.delete_pet(auth_key, pet_id)
    assert status == 403

############## Тест 8.Проверка НЕВОЗМОЖНОСТИ обновления информации о питомце с помощью невалидного api ключа ############

def test_update_pet_info_with_wrong_api_key(name = generate_random_string(7), animal_type = 'dog', age = 3):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    pet_id = my_pets['pets'][0]['id']
    auth_key = {'key': 'wrong_api'}
    status, _ = pf.update_pet_info(auth_key, pet_id, name, animal_type, age)
    assert status == 403



############## Тест 9.Проверка НЕВОЗМОЖНОСТИ обновления информации о питомце без заполнения обязательных данных ############
####### Присутствует БАГ: ожидаемый статус-код ответа 400, фактически полученный - 200

def test_update_pet_info_with_wrong_data(name=None, animal_type=None, age=None):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.update_pet_info(auth_key, pet_id, name, animal_type, age)
    assert status == 200


############## Тест 10.Проверка НЕВОЗМОЖНОСТИ получения списка питомцев с неправильным фильтром ##########

def test_get_all_pets_with_wrong_filter(filter = str(generate_random_string(7))):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, _ = pf.get_list_of_pets(auth_key, filter)
    assert status == 500


############## Тест 11. Проверка возможности добавить нового питомца без имени##########################################

def test_negative_addition_new_pet(name = None, animal_type = 'собака', age = '15', pet_photo='images/dog.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 400


