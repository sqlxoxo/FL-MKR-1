import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt  # Підключаємо matplotlib для графіків

# Визначення вхідних змінних
temperature = ctrl.Antecedent(np.arange(10, 36, 1), 'temperature')
leaf_width = ctrl.Antecedent(np.arange(2, 13, 1), 'leaf_width')

# Визначення вихідної змінної
watering = ctrl.Consequent(np.arange(0, 13, 1), 'watering')

# Функції приналежності для температури
temperature['low'] = fuzz.trimf(temperature.universe, [10, 10, 15])
temperature['medium'] = fuzz.trimf(temperature.universe, [15, 25, 25])
temperature['high'] = fuzz.trimf(temperature.universe, [25, 35, 35])

# Функції приналежності для ширини листя
leaf_width['narrow'] = fuzz.trimf(leaf_width.universe, [2, 2, 4])
leaf_width['medium'] = fuzz.trimf(leaf_width.universe, [4, 8, 8])
leaf_width['wide'] = fuzz.trimf(leaf_width.universe, [8, 12, 12])

# Функції приналежності для кількості поливів
watering['low'] = fuzz.trimf(watering.universe, [0, 0, 2])
watering['medium'] = fuzz.trimf(watering.universe, [2, 6, 6])
watering['high'] = fuzz.trimf(watering.universe, [6, 12, 12])

# Правила нечіткої логіки
rule1 = ctrl.Rule(temperature['low'] & leaf_width['narrow'], watering['low'])
rule2 = ctrl.Rule(temperature['low'] & leaf_width['medium'], watering['low'])
rule3 = ctrl.Rule(temperature['low'] & leaf_width['wide'], watering['medium'])

rule4 = ctrl.Rule(temperature['medium'] & leaf_width['narrow'], watering['medium'])
rule5 = ctrl.Rule(temperature['medium'] & leaf_width['medium'], watering['medium'])
rule6 = ctrl.Rule(temperature['medium'] & leaf_width['wide'], watering['high'])

rule7 = ctrl.Rule(temperature['high'] & leaf_width['narrow'], watering['medium'])
rule8 = ctrl.Rule(temperature['high'] & leaf_width['medium'], watering['high'])
rule9 = ctrl.Rule(temperature['high'] & leaf_width['wide'], watering['high'])

# Створення системи управління
watering_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])
watering_simulation = ctrl.ControlSystemSimulation(watering_ctrl)

# Введення значень для симуляції
watering_simulation.input['temperature'] = 22  # Приклад: Температура 22°C
watering_simulation.input['leaf_width'] = 5    # Приклад: Ширина листя 5 см

# Обчислення результату
watering_simulation.compute()

# Виведення результату
print(f"Кількість поливів на місяць: {watering_simulation.output['watering']:.2f}")

# Візуалізація результатів
temperature.view()
leaf_width.view()
watering.view(sim=watering_simulation)

# Команда для тримання вікна з графіками відкритим
plt.show()
