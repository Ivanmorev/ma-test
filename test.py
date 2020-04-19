import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("test_pandas.csv") #Создаем новый фрейм, загружаем данные из CSV
print("1. Выводим ведомость оплаты: id - сумма")
data['earnings'] = data['price_per_job'] * data['jobs_made'] #Создаем новый столбец earnings в текущем фрейме
payroll = data.groupby(by=['uid'], as_index=False)['earnings'].sum() #Создаем новый фрейм payroll, группируя фрейм data uid и суммируя данные по колонке earnings
payroll.to_csv("1-payroll.csv",header=False,index=False)

print("Ведомость оплаты сохранена в 1-payroll.csv")
print("2. Выводим id, которые заработали больше других и в сумме заработали 60% денег")

payroll = payroll.sort_values(by='earnings', ascending=False) #Сортируем по столбцу earnings по убыванию
target_sum  = float((payroll['earnings'].sum())*0.6) #Рассчитываем 60% от общей суммы всех значений в колонке earnings
payroll['cum_sum'] = payroll['earnings'].cumsum() #Рассчитываем кумулятивную сумму в колонке cum_sum
top60 = payroll[payroll['cum_sum'] <= target_sum].loc[:,'uid'] #Создаем новый фрейм, в который попадают строки, где колонка cum_sum меньше равна 60% и берем только колонку uid
top60.to_csv("2-top60.csv",header=False,index=False)
print("Сохранили Id, которые заработали больше других и в сумме заработали 60% денег в 2-top60.csv")
print("3.  Метод поиска тех, кто заработал слишком много, с целью обнаружить неточность / подлог в исходных данных")
print("3.1  Проанализируем среднюю оплату за работу c помощью графика")
price_per_job_mean = data.groupby(by=['uid'], as_index=False)['price_per_job'].mean() # создаем фрейм, группируем по uid и считаем среднее для price_per_job
price_per_job_mean.plot(kind='bar',x='uid',y='price_per_job', title='Распределение средней з/п') #формируем график соотношения uid к средней price_per_job
plt.show()
outliers = float(input('Введите значения, превышение которых считаем отклонением, например 0.4:'))
select_by_price_per_job_mean = price_per_job_mean[price_per_job_mean['price_per_job'] >= outliers].loc[:,'uid'] #делаем выборку только тех uid,у  которых price_per_job больше введеного значения
select_by_price_per_job_mean.to_csv("3.1-select_by_price_per_job_mean.csv",header=False,index=False)
print("Сохранили ", len(select_by_price_per_job_mean), "uid, чья средняя з/п превышает или равна порогу отклонения в", outliers, "в файл 3.1-select_by_price_per_job_mean.csv")

print("3.2  Проанализируем среднюю з/п, рассчитав z-score и оставив только z-score > 3") #https://ru.wikipedia.org/wiki/Z-%D0%BE%D1%86%D0%B5%D0%BD%D0%BA%D0%B0
price_per_job_mean['z-score'] = (price_per_job_mean.price_per_job - price_per_job_mean.price_per_job.mean())/price_per_job_mean.price_per_job.std(ddof=0) #считаем z-score для price_per_job
select_by_price_per_job_mean_by_zscore  = price_per_job_mean[price_per_job_mean['z-score'] > float(3)].loc[:,'uid'] #берем превышаюшие значение 3 для z-score, так как нас интересует только превышение
select_by_price_per_job_mean_by_zscore.to_csv("3.2-select_by_price_per_job_mean_z-score.to_csv",header=False,index=False)
print("Сохранили ", len(select_by_price_per_job_mean_by_zscore), "uid,  z-score которых превышает 3, в 3.2-select_by_price_per_job_mean_z-score.csv")
