def project1():
    """import pandas as pd
import numpy as np
from scipy import stats
from scipy.stats import t
from scipy.stats import f
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression


df = pd.read_excel('GDP_Unemployment_1.xlsx')
df.rename(columns={'Unnamed: 0': 'Год'}, inplace=True)
df.rename(columns={'GDP (in billion USD)': 'ВВП (млрд долл.)'}, inplace=True)
df.rename(columns={'Unemployment Rate (%)': 'Уровень безработицы (%)'}, inplace=True)
df


GDP = df.iloc[:, 1].to_numpy()
Unemployment = df.iloc[:, 2].to_numpy()
n = len(GDP)
GDP, Unemployment


# Анализ закона


years = np.arange(1993, 2024)
fig, ax1 = plt.subplots(figsize=(12, 6))
color = 'r'
ax1.set_xlabel('Год')
ax1.set_ylabel('ВВП (млрд долл.)', color=color)
ax1.plot(years, GDP, color=color, marker='o', label='ВВП (млрд долл.)')
ax1.tick_params(axis='y', labelcolor=color)
ax1.grid(True)
ax2 = ax1.twinx()
color = 'b'
ax2.set_ylabel('Уровень безработицы (%)', color=color)
ax2.plot(years, Unemployment, color=color, marker='o', label='Уровень безработицы (%)')
ax2.tick_params(axis='y', labelcolor=color)
plt.title('ВВП и Уровень безрабитицы в Финляндии (1993 - 2023)')
fig.tight_layout()
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')
plt.show()


# 1) Расчетать Гxy, проверить его значение


gamma, p_value  = stats.pearsonr(Unemployment, GDP)
print(f'Коэффицент корреляции: {gamma}')
t_rasch_abs = stats.t.ppf(1 - p_value / 2, n - 2)
print(f'Расчетное распределение стъюдента по модулю: {t_rasch_abs}')
alpha = 0.05
t_tabl = t.ppf(1 - alpha / 2, n - 2)
print(f'Табличное распределение стъюдента: {t_tabl}')
# => H0 отвергается, => в P=0,95 можно утверждать, что связь обратная и сильная


# 2) построение уравнения парной линейной регрессии


def regression_std(y, y_pred, n):
    return (np.sum((y - y_pred)**2) / (n - 2))**0.5
def create_S_b0(S, x, n):
    return S * (np.sum(x**2) / (n * np.sum((x - x.mean())**2)))**0.5
def create_S_b1(S, x):
    return S * (1 / np.sum((x - x.mean())**2))**0.5
model = LinearRegression()
model.fit(Unemployment.reshape(-1, 1), GDP.reshape(-1, 1))
b0 = model.intercept_[0]
b0
b1 = model.coef_[0][0]
b1
y_pred = model.predict(X.reshape(-1, 1))
S = regression_std(GDP, y_pred, n)
S
S_b0 = create_S_b0(S, Unemployment, n)
S_b0
S_b1 = create_S_b1(S, Unemployment)
S_b1
t_rasch_b0 = b0 / S_b0
t_rasch_b0, t_tabl
# => H0 отвергается => b0 статистически значимо
t_rasch_b1 = b1 / S_b1
abs(t_rasch_b1), t_tabl
# => H0 отвергается => b1 статистически значимо


# 3) проверить значимость уравнения


alpha = 0.95
nu_1 = 1
F_tabl = f.ppf(alpha, nu_1, n - 2)
F_rasch = (n - 2)*gamma**2 / (1 - gamma**2)
F_rasch, F_tabl
# => H0 отвергается => ур-е регрессии статистически значимо


xx = np.linspace(Unemployment.min(), Unemployment.max(), 100).reshape(-1, 1)
yy = model.predict(xx)
line_eq = f"Y = {b0} + {b1}X"
plt.figure(figsize=(8, 6))
plt.scatter(Unemployment, GDP, color='red', marker='x')
plt.plot(xx, yy, 'b-', label=line_eq)
plt.xlabel("ВВП (млрд долл.)")
plt.ylabel("Уровень безработицы (%)")
plt.title("Зависимость уровня ВВП от безработицы")
plt.legend()
plt.grid(True)
plt.show()"""


def project2():
    """import pandas as pd
import numpy as np
from scipy import stats
from scipy.stats import t
from scipy.stats import f
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression


df = pd.read_excel('Домашнее задание №2 ММР.xlsx', skiprows=1).iloc[:, 2:9]


# отчищаем от выбросов df


'''
#ф-я с for
def remove_outliers(df, upper_bound):
    # Вычисление средних значений для каждого столбца
    mean_values = df.mean()
    # Замена выбросов на средние значения
    for column in df.columns:
        df[column] = df[column].apply(lambda x: mean_values[column] if x > upper_bound[column] else x)
    return df
'''
def remove_outliers(df, upper_bound):
  mean_values = df.mean()
  df = df.mask(df > upper_bound, mean_values, axis=1)
  return df
df_new = (remove_outliers(df, upper_bound)).round(3)
plt.figure(figsize=(12, 8))
plt.boxplot(df_new)
plt.title('После выбросов')
plt.show()


# №2


#до удаления выбросов
plt.figure(figsize=(15, 10))
for i, column in enumerate(df.columns[1:], 1):
    plt.subplot(2, 3, i)
    plt.scatter(df[column], df['Y'])
    plt.title(f'Y vs {column}')
    plt.xlabel(column)
    plt.ylabel('Y')

plt.tight_layout()
plt.show()
#после удаления выбросов
plt.figure(figsize=(15, 10))
for i, column in enumerate(df_new.columns[1:], 1):
    plt.subplot(2, 3, i)
    plt.scatter(df_new[column], df_new['Y'])
    plt.title(f'Y vs {column}')
    plt.xlabel(column)
    plt.ylabel('Y')

plt.tight_layout()
plt.show()


# №3
#корреляционная матрица
df_new.corr()


# строим начальную модель со всеми, в том числе незначимыми иксами


x = df_new.iloc[:, 1:]
y = df_new['Y']
df_new

model = LinearRegression().fit(x, y)
y_pred = model.predict(x)
residuals = y - y_pred
n = len(y)
k = x.shape[1]
mse = np.sum(residuals**2) / (n - k - 1)
x_with_const = np.c_[np.ones(n), x]
cov_matrix = mse * np.linalg.inv(x_with_const.T @ x_with_const)
std_errors = np.sqrt(np.diag(cov_matrix))
t_stats = model.coef_ / std_errors[1:]
p_values = [2 * (1 - stats.t.cdf(np.abs(t), n - k - 1)) for t in t_stats]
alpha = 0.05
t_critical = stats.t.ppf(1 - alpha / 2, n - k - 1)
results = []
for i, (coef, se, t, p) in enumerate(zip(model.coef_, std_errors[1:], t_stats, p_values)):
    significance = "Значимый" if abs(t) > t_critical else "Незначимый"
    results.append((f"{df_new.columns[1+i]}", coef, se, t, p, t_critical, significance))
results_df = pd.DataFrame(results, columns=['Factor', 'Coefficient', 'Std Error', 't-statistic', 'p-value', 't-critical', 'Significance'])
results_df


# удаляем самый незначимый X (X1, т.к. самое высокое p-value) и повторяем все заново


df_with_5_X = df_new.drop('X1', axis=1)
x = df_with_5_X.iloc[:, 1:]
y = df_with_5_X['Y']
model = LinearRegression().fit(x, y)
y_pred = model.predict(x)
residuals = y - y_pred
n = len(y)
k = x.shape[1]
mse = np.sum(residuals**2) / (n - k - 1)
x_with_const = np.c_[np.ones(n), x]
cov_matrix = mse * np.linalg.inv(x_with_const.T @ x_with_const)
std_errors = np.sqrt(np.diag(cov_matrix))
t_stats = model.coef_ / std_errors[1:]
p_values = [2 * (1 - stats.t.cdf(np.abs(t), n - k - 1)) for t in t_stats]
alpha = 0.05
t_critical = stats.t.ppf(1 - alpha / 2, n - k - 1)
results = []
for i, (coef, se, t, p) in enumerate(zip(model.coef_, std_errors[1:], t_stats, p_values)):
    significance = "Значимый" if abs(t) > t_critical else "Незначимый"
    results.append((f"{df_with_5_X.columns[1+i]}", coef, se, t, p, t_critical, significance))
results_df = pd.DataFrame(results, columns=['Factor', 'Coefficient', 'Std Error', 't-statistic', 'p-value', 't-critical', 'Significance'])
results_df


# удаляем самый незначимый X (X6, т.к. самое высокое p-value) и повторяем все заново


df_with_4_X = df_with_5_X.drop('X6', axis=1)
x = df_with_4_X.iloc[:, 1:]
y = df_with_4_X['Y']
model = LinearRegression().fit(x, y)
y_pred = model.predict(x)
residuals = y - y_pred
n = len(y)
k = x.shape[1]
mse = np.sum(residuals**2) / (n - k - 1)
x_with_const = np.c_[np.ones(n), x]
cov_matrix = mse * np.linalg.inv(x_with_const.T @ x_with_const)
std_errors = np.sqrt(np.diag(cov_matrix))
t_stats = model.coef_ / std_errors[1:]
p_values = [2 * (1 - stats.t.cdf(np.abs(t), n - k - 1)) for t in t_stats]
alpha = 0.05
t_critical = stats.t.ppf(1 - alpha / 2, n - k - 1)
results = []
for i, (coef, se, t, p) in enumerate(zip(model.coef_, std_errors[1:], t_stats, p_values)):
    significance = "Значимый" if abs(t) > t_critical else "Незначимый"
    results.append((f"{df_with_4_X.columns[1+i]}", coef, se, t, p, t_critical, significance))
results_df = pd.DataFrame(results, columns=['Factor', 'Coefficient', 'Std Error', 't-statistic', 'p-value', 't-critical', 'Significance'])
results_df


# удаляем самый незначимый X (X5, т.к. самое высокое p-value) и повторяем все заново


df_with_3_X = df_with_4_X.drop('X5', axis=1)
x = df_with_3_X.iloc[:, 1:]
y = df_with_3_X['Y']
model = LinearRegression().fit(x, y)
y_pred = model.predict(x)
residuals = y - y_pred
n = len(y)
k = x.shape[1]
mse = np.sum(residuals**2) / (n - k - 1)
x_with_const = np.c_[np.ones(n), x]
cov_matrix = mse * np.linalg.inv(x_with_const.T @ x_with_const)
std_errors = np.sqrt(np.diag(cov_matrix))
t_stats = model.coef_ / std_errors[1:]
p_values = [2 * (1 - stats.t.cdf(np.abs(t), n - k - 1)) for t in t_stats]
alpha = 0.05
t_critical = stats.t.ppf(1 - alpha / 2, n - k - 1)
results = []
for i, (coef, se, t, p) in enumerate(zip(model.coef_, std_errors[1:], t_stats, p_values)):
    significance = "Значимый" if abs(t) > t_critical else "Незначимый"
    results.append((f"{df_with_4_X.columns[1+i]}", coef, se, t, p, t_critical, significance))
results_df = pd.DataFrame(results, columns=['Factor', 'Coefficient', 'Std Error', 't-statistic', 'p-value', 't-critical', 'Significance'])
results_df


# Остался DataFrame df_with_3_X, где X2, X3, X4 статистически значимы


results_df

plt.figure(figsize=(8, 6))
plt.scatter(y_pred, y, color='blue', marker='o', label='Predicted vs Actual')
plt.plot(y, y, color='red', linestyle='--', label='Ideal Fit (y = y_pred)')
plt.title('После выкидывания незначимых X', fontsize=16)
plt.xlabel('Predicted Values', fontsize=14)
plt.ylabel('Actual Values', fontsize=14)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize=12)
plt.xlim([min(y_pred.min(), y.min()), max(y_pred.max(), y.max())])
plt.ylim([min(y_pred.min(), y.min()), max(y_pred.max(), y.max())])
plt.show()

model.score(x, y)"""


def project3():
    """import pandas as pd
import numpy as np
from scipy import stats
from scipy.stats import t
from scipy.stats import f
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from scipy.stats import pearsonr


# ЛИСТ 2


df = pd.read_excel('Дз 3 нелинейная.xlsx', sheet_name='Лист2').iloc[:, 1:]
df = df.rename(columns={
    'Unnamed: 1': 'Y',
    'Unnamed: 2': 'X'
})
df['Ln_x'] = np.log(df['X'])
df['Ln_y'] = np.log(df['Y'])
df

x, y = np.array(df['Ln_x']).reshape(-1, 1), df['Ln_y']
list_2_model = LinearRegression().fit(x, y)
b0, b1 = list_2_model.intercept_, list_2_model.coef_[0]
print(b0, b1)
print(list_2_model.score(x, y))

y_pred = list_2_model.predict(x)
plt.scatter(y_pred, y, color='blue', label='Predicted vs Actual')
plt.plot([min(y_pred), max(y_pred)], [min(y_pred), max(y_pred)], color='red', linestyle='--', label='Ideal Fit (y = y_pred)')
plt.xlabel('Predicted Values')
plt.ylabel('Actual Values')
plt.legend()
plt.grid(True)
plt.show()


# ЛИСТ 3


df = pd.read_excel('Дз 3 нелинейная.xlsx', sheet_name='Лист3').iloc[:, 1:].rename(columns={
    'Unnamed: 1':'Y',
    'Unnamed: 2':'X'
})
df['Ln_x'] = np.log(df['X'])
df['Ln_y'] = np.log(df['Y'])
df

x, y = np.array(df['Ln_x']).reshape(-1, 1), df['Ln_y']
list_3_model = LinearRegression().fit(x, y)
b0, b1 = list_3_model.intercept_, list_3_model.coef_[0]
print(b0, b1)
print(list_3_model.score(x, y))


# Лист 4


df = pd.read_excel('Дз 3 нелинейная.xlsx', sheet_name='Лист4').iloc[:, 1:].rename(columns={
    'Q': 'Y',
    'L': 'X1',
    'K': 'X2'
})
df['Ln_y'] = np.log(df['Y'])
df['Ln_x1'] = np.log(df['X1'])
df['Ln_x2'] = np.log(df['X2'])
df

list_4_model = LinearRegression().fit(x, y)
b0, b1, b2 = list_4_model.intercept_, list_4_model.coef_[0], list_4_model.coef_[1]
print(b0, b1, b2)
print(list_4_model.score(x, y))

y_pred = list_4_model.predict(x)
plt.figure(figsize=(8, 6))
plt.scatter(y_pred, y, color='blue', marker='o', label='Predicted vs Actual')
plt.plot(y, y, color='red', linestyle='--', label='Ideal Fit (y = y_pred)')
plt.xlabel('Predicted Values', fontsize=14)
plt.ylabel('Actual Values', fontsize=14)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize=12)
plt.xlim([min(y_pred.min(), y.min()), max(y_pred.max(), y.max())])
plt.ylim([min(y_pred.min(), y.min()), max(y_pred.max(), y.max())])
plt.show()

residuals = y - y_pred
n = len(y)
k = x.shape[1]
mse = np.sum(residuals**2) / (n - k - 1)
x_with_const = np.c_[np.ones(n), x]
cov_matrix = mse * np.linalg.inv(x_with_const.T @ x_with_const)
std_errors = np.sqrt(np.diag(cov_matrix))
t_stats = list_4_model.coef_ / std_errors[1:]
p_values = [2 * (1 - stats.t.cdf(np.abs(t), n - k - 1)) for t in t_stats]
alpha = 0.05
t_critical = stats.t.ppf(1 - alpha / 2, n - k - 1)
results = []
for i, (coef, se, t, p) in enumerate(zip(list_4_model.coef_, std_errors[1:], t_stats, p_values)):
    significance = "Значимый" if abs(t) > t_critical else "Незначимый"
    results.append((f"{df.columns[1+i]}", coef, se, t, p, t_critical, significance))
results_df = pd.DataFrame(results, columns=['Factor', 'Coefficient', 'Std Error', 't-statistic', 'p-value', 't-critical', 'Significance'])
results_df


## строим значимую модель, убрав X2 в ЛИСТ 4


x = np.array(df['X1']).reshape(-1, 1)

list_4_model_fixed = LinearRegression().fit(x, y)
b0, b1 = list_4_model_fixed.intercept_, list_4_model_fixed.coef_[0]
print(b0, b1)
print(list_4_model_fixed.score(x, y))


# ЗАДАЧА 18


n = 30
mean_y = 1000
mean_x1 = 420
mean_x2 = 41.5
std_y = 27
std_x1 = 45
std_x2 = 18
r_yx1 = 0.77
r_yx2 = 0.43
r_x1x2 = 0.38

# уравнение множественной регрессии в стандартизованном масштабе
beta_1 = (r_yx1 - r_yx2 * r_x1x2) / (1 - r_x1x2**2)
beta_2 = (r_yx2 - r_yx1 * r_x1x2) / (1 - r_x1x2**2)
beta_1, beta_2

# уравнение множественной регрессии в натуральном масштабе
b1 = beta_1 * (std_y / std_x1)
b2 = beta_2 * (std_y / std_x2)
b0 = mean_y - (b1 * mean_x1) - (b2 * mean_x2)
f'y = {b0:.2f} + {b1:.2f}x1 + {b2:.2f}x2'

# множественная корреляция
gamma_2 = (r_yx1**2 + r_yx2**2 - 2 * r_yx1 * r_yx2 * r_x1x2)
gamma = gamma_2**0.5
gamma

# коэффициенты эластичности
El_x1 = b1 * (mean_x1 / mean_y)
El_x2 = b2 * (mean_x2 / mean_y)
El_x1, El_x2

# фишер
k = 2
alpha = 0.05
F_tabl = (gamma_2 / k) / ((1 - gamma_2) / (n - k - 1))
F_rasch = stats.f.ppf(1 - alpha, k, n - k - 1)
F_tabl, F_rasch"""


def project4():
    """import pandas as pd
import numpy as np
from scipy.stats import *
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm


df = pd.read_excel('GDP_Unemployment.xlsx')
X = np.array(df['Unemployment Rate (%)'])
y = np.array([
    11.6, 12.0, 9.3, 8.4, 7.0, 5.8, 2.9, 4.1, 5.1, 6.6,
    5.0, 4.5, 3.3, 3.3, 1.6, 0.4, 1.1, 1.2, 1.3, 1.3,
    3.0, 2.7, 2.0, 1.3, 0.1, 0.8, 1.3, 1.6, 3.9, 1.6,
    1.7, 3.3, 3.2, 2.2, 1.2, -0.2, 0.4, 0.8, 1.2, 1.1,
    0.4, 2.1, 7.2, 4.3
])
n = len(X)


## графики


# Гистограмма
plt.figure(figsize=(6, 4))
plt.hist(X, bins=15, density=True, alpha=0.6, color='g')
mu, std = norm.fit(X)
xmin, xmax = plt.xlim()
x = np.linspace(xmin, xmax, 100)
p = norm.pdf(x, mu, std)
plt.plot(x, p, 'k', linewidth=2)
plt.title('Гистограмма остатков')
plt.show()

# Q-Q plot
plt.figure(figsize=(6, 4))
sm.qqplot(X, line='s')
plt.title('Q-Q plot')
plt.show()


## Шапиро-Уилка


stat_sw, p_sw = shapiro(X)
print(f"Тест Шапиро-Уилка: Статистика = {stat_sw}, p-значение = {p_sw}")


## Хельвига


def helwig_test(data):
    n = len(data)
    mean = np.mean(data)
    std = np.std(data, ddof=0)
    skewness = skew(data)
    S = skewness
    K = kurtosis(data, fisher=False)
    H = (n / 6) * (S**2 + ((K - 3)**2) / 4)
    p_value = 1 - chi2.cdf(H, df=2)
    return H, p_value
stat_helwig, p_helwig = helwig_test(X)
print(f"Тест Хельвига: Статистика = {stat_helwig}, p-значение = {p_helwig}")


# Jarque-Bera


stat_jb, p_jb = jarque_bera(X)
print(f"Тест Jarque-Bera: Статистика = {stat_jb}, p-значение = {p_jb}")


# Колмогорова-Смирнова


stat_ks, p_ks = kstest(X, 'norm')
print(f"Тест Колмогорова-Смирнова: Статистика = {stat_ks}, p-значение = {p_ks}")


# Выводы
print(f"Тест Шапиро-Уилка: Статистика = {stat_sw}, p-значение = {p_sw}")
print(f"Тест Хельвига: Статистика = {stat_helwig}, p-значение = {p_helwig}")
print(f"Тест Jarque-Bera: Статистика = {stat_jb}, p-значение = {p_jb}")
print(f"Тест Колмогорова-Смирнова: Статистика = {stat_ks}, p-значение = {p_ks}")

alpha = 0.05
print("\nВыводы:")
if p_sw > alpha:
    print("Тест Шапиро-Уилка: Нет оснований отвергнуть гипотезу о нормальности.")
else:
    print("Тест Шапиро-Уилка: Гипотеза о нормальности отвергается.")
if p_helwig > alpha:
    print("Тест Хельвига: Нет оснований отвергнуть гипотезу о нормальности.")
else:
    print("Тест Хельвига: Гипотеза о нормальности отвергается.")
if p_jb > alpha:
    print("Тест Jarque-Bera: Нет оснований отвергнуть гипотезу о нормальности.")
else:
    print("Тест Jarque-Bera: Гипотеза о нормальности отвергается.")
if p_ks > alpha:
    print("Тест Колмогорова-Смирнова: Нет оснований отвергнуть гипотезу о нормальности.")
else:
    print("Тест Колмогорова-Смирнова: Гипотеза о нормальности отвергается.")


## ТЕОРИЯ


Таким образом условия применения таких тестов, как согласия Хельвига, Шапиро—
Вилька, Jarque-Bera и Колмогорова-Смирнова можно обозначить следующим образом:
1. Тест согласия Хельвига применяется на остатках модели; ограничений по размеру
выборки нет, но тест может работать по-разному на выборках разного размера;
применяется только к линейной регрессии; цель - проверить, имеют ли остатки
модели постоянную дисперсию (гомоскедастичны) и соответствуют ли условиям
применения линейной регрессии
2. Тест Шапиро—Вилька применяется на непрерывных числовых данных, которые
предполагаются нормально распределенными; рекомендуется для небольших и
средних выборок; цель - проверить нормальность распределения данных
3. Тест Джарка-Бера применяется на непрерывных числовых данных, которые
предполагаются нормально распределенными; рекомендуется для больших
выборок, так как он менее чувствителен к малым отклонениям; цель - проверить
нормальность распределения данных
4. Тест Колмогорова-Смирнова применяется на непрерывных числовых данных;
подходит для средних и больших выборок; цель - проверка соответствия
эмпирического распределения теоретическому"""


def dop():
    """# Средняя относительная ошибка аппроксимации (MAPE)


Y_pred = model.predict(X)
mape = np.mean(np.abs((Y - Y_pred) / Y)) * 100


## Теорема Гаусса-Маркова


Если выполнены все условия Гаусса-Маркова, то оценки параметров, полученные методом наименьших квадратов (МНК), обладают следующими свойствами:
1. Несмещенность, 2. Эффективность

Для того чтобы теорема Гаусса-Маркова была применима, должны выполняться следующие условия:
1. Линейность модели
2. Несмещенность ошибок (Ожидаемое значение ошибок (остатков) должно быть равно нулю)
3. Гомоскедастичность (Дисперсия ошибок должна быть постоянной и одинаковой для всех наблюдений)
4. Отсутствие автокорреляции (Ошибки должны быть независимыми друг от друга)
5. Отсутствие мультиколлинеарности (независимые переменные не должны быть линейно зависимыми друг от друга)


1. Линейность модели


from scipy.stats import linregress
# Генерация линейных данных
np.random.seed(0)
n = 100
x = np.random.rand(n)
y = 2 + 3 * x + np.random.randn(n)
# Оценка параметров линейной регрессии
slope, intercept, r_value, p_value, std_err = linregress(x, y)
# Визуализация данных и регрессии
plt.figure(figsize=(8, 6))
plt.scatter(x, y, label='Данные')
plt.plot(x, intercept + slope * x, color='red', label='Линейная регрессия')
plt.title('Линейность модели')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.show()


2. Несмещенность ошибок


# Вычисление остатков
residuals = y - (intercept + slope * x)
# Визуализация распределения остатков
plt.figure(figsize=(8, 6))
plt.hist(residuals, bins=20, edgecolor='black')
plt.title('Распределение остатков')
plt.xlabel('Остатки')
plt.ylabel('Частота')
plt.show()


3. Гомоскедастичность


# Визуализация остатков от предсказанных значений
predicted_y = intercept + slope * x
plt.figure(figsize=(8, 6))
plt.scatter(predicted_y, residuals)
plt.axhline(y=0, color='red', linestyle='--')
plt.title('Гомоскедастичность')
plt.xlabel('Предсказанные значения')
plt.ylabel('Остатки')
plt.show()


4. Отсутствие автокорреляции


from statsmodels.graphics.tsaplots import plot_acf
# Визуализация автокорреляции остатков
plt.figure(figsize=(8, 6))
plot_acf(residuals, lags=20)
plt.title('Автокорреляция остатков')
plt.show()


5. Отсутствие мультиколлинеарности


# Генерация данных с двумя независимыми переменными
np.random.seed(0)
x1 = np.random.rand(n)
x2 = 0.5 * x1 + np.random.randn(n) * 0.1  # x2 слабо коррелирует с x1
y = 2 + 3 * x1 + 4 * x2 + np.random.randn(n)
# Оценка параметров линейной регрессии
slope1, intercept1, r_value1, p_value1, std_err1 = linregress(x1, y)
slope2, intercept2, r_value2, p_value2, std_err2 = linregress(x2, y)
# Визуализация данных и регрессии
plt.figure(figsize=(8, 6))
plt.scatter(x1, y, label='Данные (x1)')
plt.scatter(x2, y, label='Данные (x2)')
plt.plot(x1, intercept1 + slope1 * x1, color='red', label='Регрессия (x1)')
plt.plot(x2, intercept2 + slope2 * x2, color='blue', label='Регрессия (x2)')
plt.title('Отсутствие мультиколлинеарности')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.show()


## Построение прогнозного доверительного интервала


# Новое значение X на 105% от среднего
X_mean = data['X'].mean()
X_new = 1.05 * X_mean

# Построим точечный прогноз и доверительный интервал
X_pred = sm.add_constant(pd.DataFrame({'X': [X_new]}))
Y_new_pred = model.get_prediction(X_pred)

# Доверительный интервал
interval = Y_new_pred.conf_int(alpha=0.05)
print(f"Точечное прогнозное значение Y: {Y_new_pred.predicted_mean[0]}")
print(f"95% доверительный интервал: [{interval[0][0]}, {interval[0][1]}]")
"""
