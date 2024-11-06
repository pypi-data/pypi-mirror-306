import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np
import statsmodels.api as sm
from statsmodels.stats.diagnostic import het_breuschpagan
from statsmodels.stats.stattools import durbin_watson
from statsmodels.regression.linear_model import OLS
from statsmodels.tools import add_constant
import seaborn as sns
from typing import Dict, Any, Optional, Tuple
from sklearn.preprocessing import PolynomialFeatures
import inspect

class EconometricAnalysis:
    def __init__(self, X: np.ndarray, y: np.ndarray, label_x: str = "X", label_y: str = "Y"):
        """Инициализация анализа эконометрической модели

        Args:
            X: независимая переменная
            y: зависимая переменная
            label_x: название независимой переменной
            label_y: название зависимой переменной
        """
        self.X = X
        self.y = y
        self.label_x = label_x  # Поменяли на label_x
        self.label_y = label_y  # Поменяли на label_y
        self.X_with_const = add_constant(X)
        self.model = OLS(y, self.X_with_const).fit()
        self.residuals = self.model.resid
        self.n = len(X)  # размер выборки

    def _get_t_for_r_critical(self, alpha=0.05) -> float:
        n = len(self.X)
        t_critical = stats.t.ppf(1 - alpha / 2, df=n - 2)
        return t_critical

    def task1_specification(self) -> Dict[str, Any]:
        """Задание 1: Спецификация модели с подробным анализом"""
        n = self.n

        # Линейная регрессия
        linear_model = sm.OLS(self.y, self.X_with_const).fit()
        linear_r_squared = linear_model.rsquared

        # Полиномиальная регрессия второй степени
        poly_features = PolynomialFeatures(degree=2)
        X_poly = poly_features.fit_transform(self.X.reshape(-1, 1))
        poly_model = sm.OLS(self.y, sm.add_constant(X_poly)).fit()

        try:
            y_log = np.log(self.y)  # Попытка логарифмирования
            exp_model = sm.OLS(y_log, sm.add_constant(self.X)).fit()
        except ValueError as e:
            print(f"Ошибка при выполнении логарифма: {e}")
            exp_model = None  # Или другая обработка
        # Логарифмическая регрессия
        try:
            # Проверяем наличие нулей или отрицательных значений в self.X
            if np.any(self.X <= 0):
                raise ValueError(
                    "В X есть нулевые или отрицательные значения. Логарифмическая регрессия не будет выполнена.")

            # Если проверка прошла успешно, выполняем логарифмическую регрессию
            log_model = sm.OLS(self.y, sm.add_constant(np.log(self.X))).fit()

        except ValueError as e:
            print(f"Ошибка при выполнении логарифмической регрессии: {e}")
            log_model = None  # Или можно использовать другую обработку
        # Гипербола
        try:
            if np.any(self.X == 0):  # Проверка на наличие нулей в self.X
                raise ValueError("В X есть нулевые значения. Гиперболическая регрессия не будет выполнена.")

            hyperbola_model = sm.OLS(self.y, sm.add_constant(1 / self.X)).fit()

        except ValueError as e:
            print(f"Ошибка при выполнении гиперболической регрессии: {e}")
            hyperbola_model = None  # Или можно использовать другую обработку

        # Рассчитываем корреляции и статистики для каждой модели
        results = {}
        models = {
            'Линейная': linear_model,
            'Полином 2 степени': poly_model,
            'Экспоненциальная': exp_model,
            'Логарифмическая': log_model,
            'Гипербола': hyperbola_model
        }

        best_model_name = 'Линейная'  # По умолчанию линейная
        best_r_squared = linear_r_squared
        best_model = linear_model  # Начинаем с линейной модели
        best_results = None  # Изменено для хранения полных результатов

        for name, model in models.items():
            if model is not None:  # Проверяем, что модель существует
                r_squared = model.rsquared
                correlation = np.corrcoef(self.y, model.fittedvalues)[0, 1]
                t_statistic = correlation * np.sqrt((n - 2) / (1 - correlation ** 2))
                t_critical = self._get_t_for_r_critical()

                # Определение силы связи
                if abs(correlation) > 0.7:
                    strength = "сильная"
                elif abs(correlation) > 0.5:
                    strength = "средняя"
                else:
                    strength = "слабая"

                result = {
                    'correlation': correlation,
                    't_statistic': t_statistic,
                    't_critical': t_critical,
                    'relationship': 'положительная' if correlation > 0 else 'отрицательная',
                    'is_significant': abs(t_statistic) > t_critical,
                    'strength': strength,  # Теперь строковое значение
                    'r_squared': r_squared,
                    'conclusion': self._generate_conclusion(correlation, t_statistic > t_critical, strength)
                }

                results[name] = result

                # Проверка на улучшение R^2 более чем на 5%
                if name != 'Линейная' and (r_squared - linear_r_squared) > 0.05:
                    best_model_name = name
                    best_r_squared = r_squared
                    best_model = model  # Сохраняем модель, а не только ее имя
                    best_results = result

        # Обновляем self.X для лучшей модели, y оставляем без изменений
        if best_model_name == 'Экспоненциальная':
            self.X = self.X  # Оставляем X без изменений
        elif best_model_name == 'Логарифмическая':
            self.X = np.log(self.X)  # Обновляем X на логарифмические значения
        elif best_model_name == 'Полином 2 степени':
            poly_features = PolynomialFeatures(degree=2)  # Создаем экземпляр PolynomialFeatures
            X_poly = poly_features.fit_transform(self.X.reshape(-1, 1))
            self.X = X_poly
            self.poly_features = X_poly
        elif best_model_name == 'Гипербола':
            self.X = 1 / self.X  # Обновляем X на гиперболические значения

        self.X_with_const = add_constant(self.X)

        # Если лучшая модель не была выбрана, используем линейную
        if best_results is None:
            best_results = results['Линейная']

        # Обработка различных моделей
        if best_model_name == 'Полином 2 степени':
            plt.scatter(self.X[:, 1], self.y, alpha=0.5, label='Данные')
            # Генерация значений X для графика
            X_range = np.linspace(self.X[:, 1].min(), self.X[:, 1].max(), 100).reshape(-1, 1)
            poly_features = PolynomialFeatures(degree=2)  # Убедитесь, что вы создаете новый экземпляр
            X_poly_range = poly_features.fit_transform(X_range)  # Преобразуем в полиномиальные значения

            # Предсказание для полиномиальной модели
            y_poly_pred = best_model.predict(X_poly_range)

            plt.plot(X_range, y_poly_pred, 'r-', label=f'{best_model_name} (R² = {best_model.rsquared:.4f})')
        else:
            # Для других моделей
            plt.scatter(self.X, self.y, alpha=0.5, label='Данные')
            plt.plot(self.X, best_model.predict(sm.add_constant(self.X)),
                     'r-', label=f'{best_model_name} (R² = {best_model.rsquared:.4f})')

        # Добавление подписей и заголовка
        plt.xlabel('Независимая переменная (X)')
        plt.ylabel('Зависимая переменная (Y)')
        plt.title('Регрессионная модель')
        plt.legend()
        plt.grid(True)
        plt.show()

        self.model = best_model
        self.model_name = best_model_name

        return {
            'results': results,
            'best_model': best_model_name,
            'best_model_results': best_results
        }

    def _generate_conclusion(self, correlation: float, is_significant: bool, strength: str) -> str:
        """Генерация текстового вывода для модели"""
        conclusion_parts = []

        if is_significant:
            conclusion_parts.append("Корреляция статистически значима (|t| > t_крит).")
            conclusion_parts.append(f"Наблюдается {strength} связь между переменными.")
            conclusion_parts.append(f"Направление связи: {'положительное' if correlation > 0 else 'отрицательное'}.")
        else:
            conclusion_parts.append("Корреляция статистически не значима.")

        return " ".join(conclusion_parts)

    def task2_model_quality(self) -> Dict[str, Any]:
        """Задание 2: Оценка качества модели"""
        # Начальная предсказанная переменная
        y_pred = self.model.predict(self.X_with_const)
        relative_error = np.mean(np.abs((self.y - y_pred) / self.y)) * 100

        # Критическое значение F-статистики
        df1 = 1  # число регрессоров
        df2 = self.n - 2  # n-k-1
        f_critical = stats.f.ppf(0.95, df1, df2)

        # Расчет фактического значения F-статистики
        f_stat = self.model.fvalue

        # Критическое значение t-статистики
        t_critical = stats.t.ppf(0.975, df2)  # двусторонний тест, α=0.05

        # Инициализация значимости коэффициентов
        significant_mask = np.ones(len(self.model.params), dtype=bool)  # Все коэффициенты значимы изначально

        # Поочередно исключаем незначимые коэффициенты
        for i in range(len(significant_mask)):
            t_stats = np.abs(self.model.tvalues)
            if t_stats[i] <= t_critical:
                print(f"Коэффициент {i} незначим и будет исключен.")
                significant_mask[i] = False

                # Создаем новую матрицу X только со значимыми регрессорами
                significant_columns = np.where(significant_mask)[0]
                if len(significant_columns) > 0:
                    X_significant = self.X[:, significant_columns]
                    X_significant = add_constant(X_significant)  # Добавляем константу
                    new_model = OLS(self.y, X_significant).fit()

                    # Обновляем модель и связанные характеристики
                    self.model = new_model
                    self.X_with_const = X_significant
                    y_pred = self.model.predict(self.X_with_const)
                    relative_error = np.mean(np.abs((self.y - y_pred) / self.y)) * 100

                    # Обновляем F-статистику и степени свободы
                    df1 = len(significant_columns) - 1  # один меньше, если исключаем константу
                    df2 = self.n - df1 - 1
                    f_critical = stats.f.ppf(0.95, df1, df2)
                    f_stat = self.model.fvalue

                    # Обновляем t-статистики
                    t_stats = np.abs(self.model.tvalues)
            else:
                # Если коэффициент значим, можем закончить проверку
                break

        # Формируем уравнение регрессии
        equation_parts = []
        if significant_mask[0]:  # если константа значима
            equation_parts.append(f'{self.model.params[0]:.4f}')

        # Добавляем значимые регрессоры
        for i, (param, is_significant) in enumerate(zip(self.model.params[1:], significant_mask[1:]), 1):
            if is_significant:
                sign = '+' if param > 0 else '-'
                equation_parts.append(f'{sign} {abs(param):.4f}x{i}')

        equation = ' '.join(equation_parts)

        return {
            'equation': equation,
            'r_squared': self.model.rsquared,
            'adj_r_squared': self.model.rsquared_adj,
            'f_stat': f_stat,
            'f_critical': f_critical,
            'relative_error': relative_error,
            't_stats': t_stats,
            't_critical': t_critical,
            'std_errors': self.model.bse,
            'significant_mask': significant_mask
        }

    def task3_normality_test(self) -> Dict[str, Any]:
        """Задание 3: Проверка нормальности остатков (тест Шапиро-Вилка)"""
        statistic, _ = stats.shapiro(self.residuals)

        # Критическое значение для теста Шапиро-Вилка
        # Приближенное значение для α=0.05
        critical_value = self._get_shapiro_critical()

        plt.figure(figsize=(12, 8))
        stats.probplot(self.residuals, dist="norm", plot=plt)
        plt.title("Q-Q Plot остатков")
        plt.show()
        plt.savefig('qq_plot.png')
        plt.close()

        plt.figure(figsize=(12, 8))
        plt.hist(self.residuals, bins='auto', density=True, alpha=0.7, color='skyblue')
        xmin, xmax = plt.xlim()
        x = np.linspace(xmin, xmax, 100)
        p = stats.norm.pdf(x, np.mean(self.residuals), np.std(self.residuals))
        plt.plot(x, p, 'k', linewidth=2)
        plt.title("Гистограмма остатков")
        plt.xlabel("Значение остатков")
        plt.ylabel("Частота")
        plt.grid(True)
        plt.show()
        plt.savefig('residuals_histogram.png')
        plt.close()

        return {
            'test_name': 'Shapiro-Wilk',
            'statistic': statistic,
            'critical_value': critical_value,
            'is_normal': statistic > critical_value,
            'mean_residuals': np.mean(self.residuals),
            'std_residuals': np.std(self.residuals)
        }

    def _get_shapiro_critical(self) -> float:
        """Получение приближенного критического значения для теста Шапиро-Вилка"""
        # Приближенные значения для α=0.05
        if self.n <= 4:
            return 0.748
        elif self.n <= 6:
            return 0.762
        elif self.n <= 8:
            return 0.805
        elif self.n <= 10:
            return 0.842
        elif self.n <= 20:
            return 0.905
        elif self.n <= 30:
            return 0.927
        elif self.n <= 50:
            return 0.947
        else:
            return 0.955

    def task4_heteroskedasticity(self) -> Dict[str, Any]:
        """Задание 4: Проверка гетероскедастичности (тест Спирмена)"""
        abs_residuals = np.abs(self.residuals)
        predicted_values = self.model.predict(self.X_with_const)
        spearman_corr, _ = stats.spearmanr(predicted_values, abs_residuals)

        # Рассчитываем t-статистику для коэффициента Спирмена
        n = len(predicted_values)
        t_stat = spearman_corr * np.sqrt((n - 2) / (1 - spearman_corr ** 2))

        # Критическое значение t-статистики
        t_critical = stats.t.ppf(0.975, n - 2)  # двусторонний тест, α=0.05

        # Определяем критическое значение для Spearman через t
        critical_value = t_critical * np.sqrt(1 / (n - 2))

        # График 1: Диагностика гетероскедастичности
        plt.figure(figsize=(12, 8))
        plt.scatter(predicted_values, abs_residuals, alpha=0.5)
        z = np.polyfit(predicted_values, abs_residuals, 1)
        p = np.poly1d(z)
        plt.plot(predicted_values, p(predicted_values), "r--", alpha=0.8)
        plt.xlabel('Прогнозируемые значения')
        plt.ylabel('Абсолютные значения остатков')
        plt.title('Диагностика гетероскедастичности')
        plt.grid(True)
        plt.show()
        plt.savefig('heteroskedasticity.png')
        plt.close()

        # График 2: График остатков
        plt.figure(figsize=(12, 8))
        plt.scatter(range(len(self.residuals)), self.residuals, alpha=0.5)
        plt.axhline(y=0, color='r', linestyle='--')
        # Добавляем границы ±2σ
        std_resid = np.std(self.residuals)
        plt.axhline(y=2 * std_resid, color='g', linestyle='--', alpha=0.5, label='±2σ')
        plt.axhline(y=-2 * std_resid, color='g', linestyle='--', alpha=0.5)
        plt.xlabel('Номер наблюдения')
        plt.ylabel('Остатки')
        plt.title('График остатков')
        plt.legend()
        plt.grid(True)
        plt.show()
        plt.savefig('residuals_plot.png')
        plt.close()

        # Проверка значимости корреляции Спирмена
        is_significant = abs(t_stat) > t_critical

        return {
            'spearman_correlation': spearman_corr,
            'critical_value': critical_value,
            't_stat': t_stat,
            't_critical': t_critical,
            'significant': is_significant,
            'residuals_std': std_resid,
            'outliers_count': np.sum(np.abs(self.residuals) > 2 * std_resid)
        }

    def _get_spearman_critical(self, alpha: float = 0.05) -> float:
        """Получение критического значения для коэффициента Спирмена"""
        # Приближенные значения для α=0.05, двусторонний тест
        if self.n <= 5:
            return 1.000
        elif self.n <= 6:
            return 0.886
        elif self.n <= 7:
            return 0.786
        elif self.n <= 8:
            return 0.738
        elif self.n <= 9:
            return 0.683
        elif self.n <= 10:
            return 0.648
        elif self.n <= 12:
            return 0.591
        elif self.n <= 14:
            return 0.544
        elif self.n <= 16:
            return 0.506
        elif self.n <= 18:
            return 0.475
        elif self.n <= 20:
            return 0.450
        elif self.n <= 22:
            return 0.428
        elif self.n <= 24:
            return 0.409
        elif self.n <= 26:
            return 0.392
        elif self.n <= 28:
            return 0.377
        elif self.n <= 30:
            return 0.364
        else:
            # Для больших выборок используем приближение
            return 2 / np.sqrt(self.n)

    def task5_autocorrelation(self) -> Dict[str, Any]:
        """Задание 5: Проверка автокорреляции (тест Дарбина-Уотсона)"""
        dw_statistic = durbin_watson(self.residuals)
        dw_critical = self._get_durbin_watson_critical()

        return {
            'dw_statistic': dw_statistic,
            'critical_values': dw_critical,
            'has_autocorrelation': (dw_statistic < dw_critical['dl'] or
                                    dw_statistic > (4 - dw_critical['dl'])),
            'inconclusive': ((dw_critical['dl'] <= dw_statistic <= dw_critical['du']) or
                             ((4 - dw_critical['du']) <= dw_statistic <= (4 - dw_critical['dl'])))
        }

    def _get_durbin_watson_critical(self) -> Dict[str, float]:
        """Получение критических значений для теста Дарбина-Уотсона"""
        # Приближенные значения для α=0.05, k=1 (один регрессор)
        if self.n <= 6:
            return {'dl': 0.610, 'du': 1.400}
        elif self.n <= 7:
            return {'dl': 0.700, 'du': 1.356}
        elif self.n <= 8:
            return {'dl': 0.763, 'du': 1.332}
        elif self.n <= 9:
            return {'dl': 0.824, 'du': 1.320}
        elif self.n <= 10:
            return {'dl': 0.879, 'du': 1.320}
        elif self.n <= 15:
            return {'dl': 1.077, 'du': 1.361}
        elif self.n <= 20:
            return {'dl': 1.201, 'du': 1.411}
        elif self.n <= 25:
            return {'dl': 1.288, 'du': 1.451}
        elif self.n <= 30:
            return {'dl': 1.352, 'du': 1.489}
        elif self.n <= 40:
            return {'dl': 1.442, 'du': 1.544}
        elif self.n <= 50:
            return {'dl': 1.503, 'du': 1.585}
        else:
            return {'dl': 1.585, 'du': 1.641}

    def task6_confidence_interval(self, exog_value: float = 1.05) -> Dict[str, Any]:
        """Задание 6: Построение доверительного интервала прогноза"""

        # Рассчитываем среднее значение X
        if self.model_name == 'Полином 2 степени':
            X_mean = np.mean(self.X_with_const[:, 1])  # Учитываем полиномиальные значения
        else:
            X_mean = np.mean(self.X_with_const)

        # Если лучшая модель - полиномиальная
        if self.model_name == 'Полином 2 степени':
            X_pred = np.array([[X_mean * exog_value]])
            poly_features = PolynomialFeatures(degree=2)
            X_poly_pred = poly_features.fit_transform(X_pred)  # Преобразуем в полиномиальные значения

            y_pred = self.model.predict(X_poly_pred)  # Предсказанное значение Y

            # Рассчитываем доверительные интервалы
            predictions = self.model.get_prediction(X_poly_pred)
            summary_frame = predictions.summary_frame(alpha=0.05)  # 95% доверительный интервал
            lower_bound = summary_frame['obs_ci_lower'][0]
            upper_bound = summary_frame['obs_ci_upper'][0]

        else:
            X_pred = sm.add_constant([[X_mean * exog_value]],
                                     has_constant='add')  # Добавляем константу с корректной формой (1, 2)
            y_pred = self.model.predict(X_pred)

            if hasattr(self.model, 'get_prediction'):
                predictions = self.model.get_prediction(X_pred)
                summary_frame = predictions.summary_frame(alpha=0.05)  # 95% доверительный интервал
                lower_bound = summary_frame['obs_ci_lower'][0]
                upper_bound = summary_frame['obs_ci_upper'][0]
            else:
                lower_bound = upper_bound = None

        return {
            'base_value': X_mean,
            'predicted_value': X_mean * exog_value,
            'prediction': y_pred[0],
            'confidence_interval': {
                'lower': lower_bound,
                'upper': upper_bound
            }
        }

    def print_full_analysis(self) -> None:
        """Вывод полного анализа с подробными выводами"""
        spec = self.task1_specification()
        print("\n=== Задание 1: Спецификация модели ===")

        # Вывод результатов для всех моделей
        for model_name, result in spec['results'].items():
            print(f"\nМодель: {model_name}")
            print(f"Коэффициент детерминации (R^2): {result['r_squared']:.4f}")
            print("Вывод:", result['conclusion'])

        # Вывод информации о наилучшей модели
        best_model = spec['best_model']
        best_results = spec['best_model_results']
        print(f"\n=== Лучшая модель: {best_model} ===")
        print(f"Коэффициент детерминации (R^2): {best_results['r_squared']:.4f}")
        print(f"Коэффициент корреляции: {best_results['correlation']:.4f}")
        print(f"t-статистика: {best_results['t_statistic']:.4f}")
        print(f"Критическое значение t: {best_results['t_critical']:.4f}")
        print(f"Характер связи: {best_results['relationship']}")
        print(f"Вывод: {best_results['conclusion']}")

        # Задание 2
        quality = self.task2_model_quality()
        print(f"\n=== Задание 2: Оценка качества модели ===")
        print(f"Уравнение регрессии: {quality['equation']}")
        print(f"R-квадрат: {quality['r_squared']:.4f}")
        print(f"Скорректированный R-квадрат: {quality['adj_r_squared']:.4f}")
        print(f"F-статистика: {quality['f_stat']:.4f}")
        print(f"Критическое значение F: {quality['f_critical']:.4f}")
        print(f"t-статистики: {quality['t_stats']}")
        print(f"Критическое значение t: {quality['t_critical']:.4f}")
        print(f"Средняя относительная ошибка аппроксимации: {quality['relative_error']:.2f}%")

        print("\nВывод о качестве модели:")
        if quality['r_squared'] > 0.8:
            print("- Модель имеет высокое качество аппроксимации")
        elif quality['r_squared'] > 0.5:
            print("- Модель имеет среднее качество аппроксимации")
        else:
            print("- Модель имеет низкое качество аппроксимации")

        if quality['f_stat'] > quality['f_critical']:
            print("- Модель статистически значима в целом (F > F_крит)")
        else:
            print("- Модель статистически не значима в целом (F < F_крит)")

        print("- Значимость коэффициентов:")
        for i, t_stat in enumerate(quality['t_stats']):
            param_name = "α" if i == 0 else "β"
            if abs(t_stat) > quality['t_critical']:
                print(f"  {param_name} статистически значим (|t| > t_крит)")
            else:
                print(f"  {param_name} статистически не значим (|t| < t_крит)")

        if quality['relative_error'] < 10:
            print("- Точность модели высокая")
        elif quality['relative_error'] < 20:
            print("- Точность модели удовлетворительная")
        else:
            print("- Точность модели низкая")

        # Задание 3
        norm = self.task3_normality_test()
        print("\n=== Задание 3: Проверка нормальности остатков ===")
        print("Обоснование выбора теста:")
        print("1) Тест Шапиро-Вилка подходит для небольшой выборки (от 2 до 50)")
        print("2) Данный тест является более универсальным и статистически мощным")
        print(f"\nСтатистика теста: {norm['statistic']:.4f}")
        print(f"Критическое значение: {norm['critical_value']:.4f}")
        print("Вывод:", end=" ")
        if norm['is_normal']:
            print("Остатки имеют нормальное распределение (W > W_крит)")
        else:
            print("Остатки не имеют нормального распределения (W < W_крит)")

        # Задание 4
        hetero = self.task4_heteroskedasticity()
        print("\n=== Задание 4: Проверка гетероскедастичности ===")
        print("Обоснование выбора теста:")
        print("1) Тест Спирмена подходит для малых выборок (n от 5 до 40)")
        print("2) Хорошо подходит для парной регрессии")
        print(f"\nКоэффициент корреляции Спирмена: {hetero['spearman_correlation']:.4f}")
        print(f"Критическое значение: {hetero['critical_value']:.4f}")
        print(f"Стандартное отклонение остатков: {hetero['residuals_std']:.4f}")

        if hetero['outliers_count'] > 0:
            print(f"Количество выбросов (>2σ): {hetero['outliers_count']}")

        print("Вывод:", end=" ")
        if hetero['significant']:
            print("Присутствует гетероскедастичность (|rs| > rs_крит)")
        else:
            print("Гомоскедастичность присутствует (|rs| < rs_крит)")

        # Задание 5
        autocorr = self.task5_autocorrelation()
        print("\n=== Задание 5: Проверка автокорреляции ===")
        print(f"Статистика Дарбина-Уотсона: {autocorr['dw_statistic']:.4f}")
        print(f"Критические значения: dL = {autocorr['critical_values']['dl']:.3f}, "
              f"dU = {autocorr['critical_values']['du']:.3f}")
        print("Вывод:", end=" ")
        if autocorr['inconclusive']:
            print("Невозможно сделать однозначный вывод о наличии автокорреляции")
        elif autocorr['has_autocorrelation']:
            if autocorr['dw_statistic'] < autocorr['critical_values']['dl']:
                print("Присутствует положительная автокорреляция")
            else:
                print("Присутствует отрицательная автокорреляция")
        else:
            print("Автокорреляция отсутствует")

        # Задание 6
        pred = self.task6_confidence_interval()
        print("\n=== Задание 6: Прогнозирование ===")
        print(f"Базовое значение {self.label_x}: {pred['base_value']:.2f}")
        print(f"Прогнозное значение {self.label_x} (105%): {pred['predicted_value']:.2f}")
        print(f"Точечный прогноз {self.label_y}: {pred['prediction']:.2f}")
        print(f"Доверительный интервал: [{pred['confidence_interval']['lower']:.2f}, ",
              f"{pred['confidence_interval']['upper']:.2f}]")

    def get_task_code(self, task_number: int) -> str:
        """Возвращает код задания по номеру.

        Args:
            task_number: номер задания

        Returns:
            str: код задания или сообщение об ошибке
        """
        task_functions = {
            1: self.task1_specification,
            2: self.task2_model_quality,
            3: self.task3_normality_test,
            4: self.task4_heteroskedasticity,
            5: self.task5_autocorrelation,
            6: self.task6_confidence_interval
        }

        task_function = task_functions.get(task_number)

        if task_function is not None:
            # Извлекаем код функции в виде строки
            code = inspect.getsource(task_function)
            return code
        else:
            return "Некорректный номер задания. Пожалуйста, введите номер от 1 до 6."
