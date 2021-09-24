from pprint import pprint
from datetime import datetime
import logging


def log_recorder(path):

    def logger(old_function):

        def new_function(*args, **kwargs):
            result = old_function(*args, **kwargs)
            print(f'Дата и время вызова функции: {datetime.now()}')
            print(f'Имя функции: {old_function.__name__}')
            print(f'Аргументы функции: {args}{kwargs}')
            pprint(f'Результат функции: {result}')
            print('----------------------------')
            logging.basicConfig(
                filename=path,
                filemode='w',
                format='%(asctime)s - %(message)s', level=logging.INFO)
            logging.info('Log is recorded to a file')
            return result
        return new_function
    return logger


with open('recipes.txt', 'r', encoding='utf-8') as f:
    cook_book = {}
    for line in f:
        dish_name = line.strip()
        count = int(f.readline().strip())
        list_of_ingredients = []
        for i in range(count):
            temp_dict = {}
            ingredient = f.readline().strip().split(' | ')
            temp_dict['ingredient_name'] = ingredient[0]
            temp_dict['quantity'] = int(ingredient[1])
            temp_dict['measure'] = ingredient[2]
            list_of_ingredients.append(temp_dict)
        cook_book[dish_name] = list_of_ingredients
        f.readline()


@log_recorder('app.log')
def get_shop_list_by_dishes(dishes, person_count):
    shop_list = {}
    for dish in dishes:
        if dish in cook_book:
            for ingredient in cook_book[dish]:
                if ingredient['ingredient_name'] in shop_list:
                    shop_list[ingredient['ingredient_name']]['quantity'] += int(ingredient['quantity'] * person_count)
                else:
                    temp_dict = {}
                    temp_dict['measure'] = ingredient['measure']
                    temp_dict['quantity'] = int(ingredient['quantity'] * person_count)
                    shop_list[ingredient['ingredient_name']] = temp_dict
    return shop_list


if __name__ == '__main__':
    get_shop_list_by_dishes(['Запеченный картофель'], 2)
    get_shop_list_by_dishes(['Фахитос'], 5)
    get_shop_list_by_dishes(['Омлет'], 3)
