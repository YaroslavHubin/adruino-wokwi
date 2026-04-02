import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pywt
from scipy.fft import fft, fftfreq
import scipy.signal as signal
from scipy.signal import find_peaks
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

df1 = pd.read_csv('Audio data.csv')
df2 = pd.read_csv('Audio data_1.csv')

df1.columns = ['Time', 'Amplitude']
df2.columns = ['Time', 'Amplitude']

plt.figure(figsize=(26, 9))

plt.subplot(1, 2, 1)
plt.plot(df1['Time'], df1['Amplitude'], color='blue')
plt.title("Сигнал з тихого місця")
plt.xlabel("Час (мс)")
plt.ylabel("Амплітуда")

plt.subplot(1, 2, 2)
plt.plot(df2['Time'], df2['Amplitude'], color='red')
plt.title("Сигнал з гучного місця")
plt.xlabel("Час (мс)")
plt.ylabel("Амплітуда")

plt.tight_layout()
plt.show()

def denoise_with_dwt(signal, wavelet='db4', level=4):
    coeffs = pywt.wavedec(signal, wavelet, level=level)
    coeffs[1:] = [np.zeros_like(c) for c in coeffs[1:]]
    reconstructed_signal = pywt.waverec(coeffs, wavelet)
    return reconstructed_signal[:len(signal)]

denoised1 = denoise_with_dwt(np.array(df1['Amplitude'].values))
denoised2 = denoise_with_dwt(np.array(df2['Amplitude'].values))

plt.figure(figsize=(14, 6))

plt.subplot(1, 2, 1)
plt.plot(df1['Time'], denoised1, color='green')
plt.title("Згладжений сигнал (тихе місце, DWT)")
plt.xlabel("Час (мс)")
plt.ylabel("Амплітуда")

plt.subplot(1, 2, 2)
plt.plot(df2['Time'], denoised2, color='orange')
plt.title("Згладжений сигнал (гучне місце, DWT)")
plt.xlabel("Час (мс)")
plt.ylabel("Амплітуда")

plt.tight_layout()
plt.show()

def get_sampling_rate(time_series):
    return 1000 / np.mean(np.diff(time_series))

fs1 = get_sampling_rate(df1['Time'])
fs2 = get_sampling_rate(df2['Time'])

def perform_fft(signal_data, fs):
    N = len(signal_data)
    yf = fft(signal_data)
    xf = fftfreq(N, 1/fs)
    return xf[:N // 2], np.abs(yf[:N // 2])

xf1, yf1 = perform_fft(df1['Amplitude'].values, fs1)
xf2, yf2 = perform_fft(df2['Amplitude'].values, fs2)

plt.figure(figsize=(14, 6))

plt.subplot(1, 2, 1)
plt.plot(xf1, yf1, color='purple')
plt.title("Фур'є-спектр (тихе місце)")
plt.xlabel("Частота (Гц)")
plt.ylabel("Амплітуда")

plt.subplot(1, 2, 2)
plt.plot(xf2, yf2, color='brown')
plt.title("Фур'є-спектр (гучне місце)")
plt.xlabel("Частота (Гц)")
plt.ylabel("Амплітуда")

plt.tight_layout()
plt.show()

scales = np.arange(1, 128)

cwtmatr1, freqs1 = pywt.cwt(df1['Amplitude'].values, scales, 'morl')
cwtmatr2, freqs2 = pywt.cwt(df2['Amplitude'].values, scales, 'morl')

plt.figure(figsize=(14, 6))

plt.subplot(1, 2, 1)
plt.imshow(cwtmatr1, extent=[df1['Time'].min(), df1['Time'].max(), scales.min(), scales.max()],
           cmap='PRGn', aspect='auto',
           vmax=abs(cwtmatr1).max(), vmin=-abs(cwtmatr1).max())
plt.title("CWT (тихе місце, Morlet wavelet)")
plt.xlabel("Час (мс)")
plt.ylabel("Масштаб")

plt.subplot(1, 2, 2)
plt.imshow(cwtmatr2, extent=[df2['Time'].min(), df2['Time'].max(), scales.min(), scales.max()],
           cmap='PRGn', aspect='auto',
           vmax=abs(cwtmatr2).max(), vmin=-abs(cwtmatr2).max())
plt.title("CWT (гучне місце, Morlet wavelet)")
plt.xlabel("Час (мс)")
plt.ylabel("Масштаб")

plt.tight_layout()
plt.show()

peaks1, _ = find_peaks(df1['Amplitude'], height=0)
peaks2, _ = find_peaks(df2['Amplitude'], height=0)

plt.figure(figsize=(14, 6))

plt.subplot(1, 2, 1)
plt.plot(df1['Time'], df1['Amplitude'], label='Сигнал')
plt.plot(df1['Time'].iloc[peaks1], df1['Amplitude'].iloc[peaks1], "x", label='Піки', color='red')
plt.title("Піки сигналу (тихе місце)")
plt.xlabel("Час (мс)")
plt.ylabel("Амплітуда")
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(df2['Time'], df2['Amplitude'], label='Сигнал')
plt.plot(df2['Time'].iloc[peaks2], df2['Amplitude'].iloc[peaks2], "x", label='Піки', color='red')
plt.title("Піки сигналу (гучне місце)")
plt.xlabel("Час (мс)")
plt.ylabel("Амплітуда")
plt.legend()

plt.tight_layout()
plt.show()

def extract_features(signal):
    mean = np.mean(signal)
    std = np.std(signal)
    var = np.var(signal)
    amp = np.max(signal) - np.min(signal)
    median = np.median(signal)
    energy = np.sum(np.square(signal))
    return {
        'Середнє': mean,
        'Стандартне відхилення': std,
        'Дисперсія': var,
        'Амплітуда': amp,
        'Медіана': median,
        'Енергія': energy
    }

features1 = extract_features(df1['Amplitude'].values)
features2 = extract_features(df2['Amplitude'].values)

print("Статистичні ознаки для тихого місця:")
for k, v in features1.items():
    print(f"{k}: {v:.4f}")

print("\nСтатистичні ознаки для гучного місця:")
for k, v in features2.items():
    print(f"{k}: {v:.4f}")

def apply_kmeans(signal_data, n_clusters=3):
    signal_reshaped = signal_data.reshape(-1, 1)
    kmeans = KMeans(n_clusters=n_clusters, random_state=0)
    labels = kmeans.fit_predict(signal_reshaped)
    return labels, kmeans

labels1, kmeans1 = apply_kmeans(df1['Amplitude'].values)
labels2, kmeans2 = apply_kmeans(df2['Amplitude'].values)

plt.figure(figsize=(14, 6))

plt.subplot(1, 2, 1)
plt.scatter(df1['Time'], df1['Amplitude'], c=labels1, cmap='viridis', s=10)
plt.title("KMeans кластеризація (тихе місце)")
plt.xlabel("Час (мс)")
plt.ylabel("Амплітуда")

plt.subplot(1, 2, 2)
plt.scatter(df2['Time'], df2['Amplitude'], c=labels2, cmap='viridis', s=10)
plt.title("KMeans кластеризація (гучне місце)")
plt.xlabel("Час (мс)")
plt.ylabel("Амплітуда")

plt.tight_layout()
plt.show()

def perform_linear_regression(time, amplitude):
    time = time.values.reshape(-1, 1)
    amplitude = amplitude.values
    model = LinearRegression()
    model.fit(time, amplitude)
    predicted = model.predict(time)
    return model, predicted

model1, pred1 = perform_linear_regression(df1['Time'], df1['Amplitude'])
model2, pred2 = perform_linear_regression(df2['Time'], df2['Amplitude'])

plt.figure(figsize=(14, 6))

plt.subplot(1, 2, 1)
plt.plot(df1['Time'], df1['Amplitude'], label='Справжній сигнал', alpha=0.6)
plt.plot(df1['Time'], pred1, color='red', label='Лінійна регресія')
plt.title("Тренд шуму (тихе місце)")
plt.xlabel("Час (мс)")
plt.ylabel("Амплітуда")
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(df2['Time'], df2['Amplitude'], label='Справжній сигнал', alpha=0.6)
plt.plot(df2['Time'], pred2, color='red', label='Лінійна регресія')
plt.title("Тренд шуму (гучне місце)")
plt.xlabel("Час (мс)")
plt.ylabel("Амплітуда")
plt.legend()

plt.tight_layout()
plt.show()

def forecast_noise(time, amplitude):
    X = time.values.reshape(-1, 1)
    y = amplitude.values
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print("Прогнозна модель:")
    print(f"  MSE: {mse:.4f}")
    print(f"  R² : {r2:.4f}")
    
    return model, X_test, y_test, y_pred

print("\nПрогноз (тихе місце):")
forecast_noise(df1['Time'], df1['Amplitude'])

print("\nПрогноз (гучне місце):")
forecast_noise(df2['Time'], df2['Amplitude'])
