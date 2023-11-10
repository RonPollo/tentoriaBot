async def get_report(state):
    async with state.proxy() as data:
                
        if data['washing_type'] == 'Наличные':
            washing_count = data['washing']
        else:
            washing_count = 0
        
        if data['azs_type'] == 'Наличные':
            azs_count = data['azs']
        else:
            azs_count = 0

        total_cash = data['yandex_nal'] + data['cash_bavaria'] - washing_count - azs_count

        total_shift = data['terminal'] + data['viza_discount'] + data['cash_bavaria'] + data['cash_card'] + data['znf'] + data['perscash'] + data['bonuse'] + data['yandex_nal'] + data['yandex_bez']
        total_shift = round(total_shift, 2)

        kof = round(total_shift / (data['last_distance'] - data['first_distance']), 2)
        report = f'''
                Номер машины: {data['number_car']}
                
                Дата: {data['date']}, {data['period']}

                Пробег начало: {data['first_distance']}
                Пробег конец: {data['last_distance']}

                Z отчет: {data['z_index']}

                Наличные Бавария: {data['cash_bavaria']}

                Терминал: {data['terminal']}

                Visa скидка: {data['viza_discount']}

                Карта онлайн: {data['cash_card']}

                ЗНФ: {data['znf']}

                Личный счет: {data['perscash']}

                Бонусы: {data['bonuse']}

                Яндекс наличные: {data['yandex_nal']}

                Яндекс безнал: {data['yandex_bez']}

                Мойка: {data['washing']}
                    тип: {data['washing_type']}

                Заправка: {data['azs']}
                    тип: {data['azs_type']}

                Всего налички: {total_cash}

                Итого за смену: {total_shift}

                Остаток воды: {data['water']}

                Посадки Яндекс: {data['count_yandex']}
                
                Посадки Бавария: {data['count_bavaria']}

                Сдано: {data['over_cash']}

                КЭФ: {kof}

                '''
    
    return report