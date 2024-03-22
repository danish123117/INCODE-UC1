import time
from scipy import signal
import json
import requests
import numpy as np

def ngsi_get(entity , window_length):# takes last 5000 data points --> this can be refined so as to fetch only values 
    url = 'http://localhost:8668/v2/entities/' + entity
    headers = {
        'Accept': 'application/json',
        'Fiware-Service': 'openiot',
        'Fiware-ServicePath': '/'
    }
    params = {
        'lastN': window_length
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return 0

def data_to_np(data):
    parsed_data = []
    for js in data:
        if not js:
            print("JSON data is empty or missing")
            continue
        try:
            batch = json.loads(js) 
        except json.decoder.JSONDecodeError as e:
            print(f"JSON decoding error: {e}")
            continue
        if "data" in batch:
            data = batch["data"]
            parsed_data.append([
                (data["ch 1"])['value'],
                (data["ch 2"])['value'],
                (data["ch 3"])['value'],
                (data["ch 4"])['value'],
                (data["ch 5"])['value'],
                (data["ch 6"])['value'],
                (data["ch 7"])['value'],
                (data["ch 8"])['value']
            ])
    numpy_arr = np.array(parsed_data).T
    return numpy_arr

def data_filter(data_arr):# Applies filteration to
    Sampling_frequency = 1000
    band_lo = 20
    band_hi = 450
    Niquist_frequency = Sampling_frequency/2
    nor_band_lo = band_lo/Niquist_frequency
    nor_band_hi = band_hi/Niquist_frequency
    del_freq = 50
    nor_del_freq = del_freq/Niquist_frequency
    Quality = 30 
    sos_band = signal.iirfilter(4, [ nor_band_lo, nor_band_hi],btype='band', ftype='butter', output = "sos")
    b, a = signal.iirnotch(nor_del_freq, Quality, Sampling_frequency)
    filtered_band = np.array(signal.sosfiltfilt(sos_band , dat_arr))
    filtered = signal.lfilter(b, a, filtered_band)
    return filtered # test this

def out_stft(filtered): # Apply stft and extract requisite features.
    frequency_domain = np.fft.fft(filtered, axis=0)
    magnitude_spectrum = np.abs(frequency_domain)
    N = filtered.shape[0]
    sampling_rate = 1 / 1000
    frequency_bins = np.fft.fftfreq(N, d=sampling_rate)
    positive_frequencies = frequency_bins[:N//2]
    mean_frequencies = np.sum(magnitude_spectrum[:N//2] * positive_frequencies[:, np.newaxis], axis=0) / np.sum(magnitude_spectrum[:N//2], axis=0)
    mean_power_frequencies = np.sum(magnitude_spectrum[:N//2] * positive_frequencies[:, np.newaxis]**2, axis=0) / np.sum(magnitude_spectrum[:N//2], axis=0)
    cumulative_power = np.cumsum(magnitude_spectrum[:N//2], axis=0)
    half_power = np.sum(magnitude_spectrum[:N//2], axis=0) / 2
    median_indices = np.argmax(cumulative_power > half_power, axis=0)
    median_frequencies = positive_frequencies[median_indices]
    #print("Mean Frequencies:", mean_frequencies)
    #print("Median Frequencies:", median_frequencies)
    #print("Men Power frequency:", median_frequencies) 
    return median_frequency , mean_frequency , mean_power_frequency # test this
    
    
def stress_out(f_mean, f_median, f_power, parms): #gives output stress level# should be generalised to n sensors rather than
    s_mean = []
    s_med= []
    s_mpower = []
    p_mean= parms["meanFrequency"]
    p_med= parms["medianFrequency"]
    p_pow= parms["meanPowerFrequency"]
    for i in range(len(f_mean)):
        ch = "c" +str(i+1)
        s_mean.append([p_mean[ch]/f_mean[i]])
        s_med.append([p_med[ch]/f_median[i]])
        s_mpower.append([p_pow[ch]/f_power[i]])
    return s_mean, s_med, s_mpower

def stress_payload(s_mean, s_med, s_mpower):
    data_lists = [s_med, s_mean, s_mpower]
    keys = ["medianFrequencyState", "meanFrequencyState", "meanPowerFrequencyState"]
    for data, key in zip(data_lists, keys):
        payload_raw[key] = {"ch{}".format(i+1): value for i, value in enumerate(data)}
    return payload_raw
    
def ngsi_patch(entity,d):#updates latest values
    url = 'http://localhost:1026/v2/entities/' + entity +'/attrs?type=Stress'

    headers = {
        'Content-Type': 'application/json'
    }
    data = d
    response = requests.patch(url, headers=headers, json=data)