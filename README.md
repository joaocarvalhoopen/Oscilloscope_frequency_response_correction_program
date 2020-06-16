# Oscilloscope frequency response correction program

This is a program that tries to make "normal scopes", give a more accurate and more real representation of the actual signals. 

## Description

This is a project to correct (equalize) the scope frequency response of "many scopes" in a PC program that is connected to the scope by USB or LAN. <br>
When it is done (this project is on going), it will make a frequency domain equalization that will correct the scopes model specific frequency response. The amplitude attenuation and the phase-shift at each frequency that the input signal is composed. Limited by the scope characteristics. Then it will reconstruct the time domain signal so that it can be visualized, analyzed and uploaded to the scope REF_A channel, for direct comparison with other signals. <br>
This is nothing new, a similar equalization is made in the MIMO WiFi Routers and 5G mobile phones to reverse the effects of multi-path. One of it's implementation is called SC-FME (Single Carrier - Frequency Domain Equalization).

## Please see this project **EEVBlog thread** where many of the concepts that will be used are heavily detailed with history  

I put it under **Test Equipment**.<br>
Topic: **Oscilloscope frequency response correction program** <br>
[https://www.eevblog.com/forum/testgear/oscilloscope-frequency-response-correction-program/](https://www.eevblog.com/forum/testgear/oscilloscope-frequency-response-correction-program/) <br>

## Components that influence a scope frequency response because they are on the signal path

- Scope probe frequency response or connected coaxial cable frequency response.
- Input impedance selected (1 M Ohm or 50 Ohms)
- Scope low noise amplifier frequency response in the front end.
- Anti-aliasing filter before the input of the sampling ADC.
- ADC (Analog to Digital Converter) sampling rate and general characteristics.
<br>
All those factors contribute to the frequency response of a scope. But they can be measured (characterized), and inverted or reversed by applying **FDE - Frequency Domain Equalization**. <br>
See the **this project EEVBlog thread** for methods of characterizing the amplitude and the phase-shift for each frequency. That is characterizing the frequency response of the scope.

## Steps needed

1. For a given model, get the scope frequency response characterization from 0 Hz to half the ADC sampling frequency. This in terms of amplitude attenuation and phase-shift characterization at each frequency. Ideally a frequency sweep, but can also be in steps.
2. Automate the frequency response characterization (this is optional, but a really good idea for fast characterization of different probes, or coaxial cables, this can also be made by the community and the info used as simple data file for the program). 
3. The program connects to the scope via PyVisa open source library.
4. The processing will be ...
   1. Read the buffer from the scope by USB or LAN.
   2. Do an FFT(signal), Fast Fourier Transform on the signal and transform it from the time domain (voltage amplitude vs time) into the frequency domain (amplitude vs frequency and phase-shift vs frequency).
   3. In the frequency domain, apply to each frequency apply the inverse of the attenuation and phase-shift at each frequency and correct or equalize the signal. Note that this is not as simple as it locks. Mainly, because of FFT inter centered bin frequency components of the signal (give raise to inter bin leakage) and because of the fact that the use of pré-processing windows, would alter the quality of the signal reconstruction. In the frequency domain the use of machine learning to learn a general mapping of frequency equalization from fine grained characterization, could also be used. 
   4. Then, do an iFFT( ), inverse Fast Fourier Transform on the frequency domain representation of the signal and reconstruct the original signal in the time domain. But more accurately, more close to the real signal.
   5. Show it on the PC in a graph plot, so you can analyze it.
5. Send it to the scope REF_A channel for comparison with other signals, if you want. 

## Oscilloscopes targeted

In principal the same method could be applied to any scope brand or model. The only thing that should change would be the scope frequency response characterization profile and the specific way the program connects to the scope. But PyVisa supports many brands and different models, by USB and by LAN. 

### **A** - Siglent SDS2104-Plus 100 MHz - equalization from 0 Hz up to 945 MHz 

This is the first scope model that I will be targeting with the software. It is a 100 MHz Siglent SDS2104-Plus with 2 ADC's, each with 2 Gig sample / sec. Having a resolution of 8 bits. This model can have a small hack that gives puts the -3dB attenuation mark on the 570 MHz (bandwidth). It's frontend, allows this scope to be used to analyse signals of up to 945 MHz. But with great attenuation. If the signal frequency components are only amplitude attenuated and phase-shifted at each frequency, that effects, in principal can be corrected or reversed. This is a normal scope effect, but if corrected (frequency domain equalized), the signal can be reconstructed with more fidelity up to it's frontend max limit of of 945 MHz. Each of the 2 ADC's are shared by each pair of 2 channels, totalizing 4 channels. If you use only one channel from the first pair (channel 1 or channel 2), and one channel from the second pair (channel 3 or channel 4), you will have the maximum possible frequency on two channels simultaneously.

### **B** - Rigol DS1104Z 100 MHz - equalization from 0 Hz maybe up to 300 MHz or 400 MHz

This will be the second scope that I will target with this program.
This scope as a bandwidth of 100 MHz at -3dB attenuation but in principal, it can be used to analyze signal of up to 300 MHz or 400 MHz. But they will be heavily attenuated and phase-shifted. The some program, with a different scope profile characterization, in principal will also correct this effect. This scope as a one 8 bit ADC at 1 Gig sample / second that is shared among all 4 channels. 

### **C** - Siglent SDS1104X-E 100 MHz - equalization from 0 Hz maybe to 300 MHz or 400 MHz

There is the possibly that this is the third scope that I will be targeting with this program. This scope as two 8 bit ADC of 1 Gig sample / second used for each of the 2 pairs of channels, totalizing 4 channels. 

### **D** - Other possible scopes targeted by the program directly by me

- Rigol DS1052E 50 MHz
- Hantek 100 MHz 


# Current progress....

## **A** - Siglent SDS2104-Plus .... current progress

This code is under the directory. <br>
[Siglent_SDS2104_Plus directory](./Siglent_SDS2104_Plus/) <br>

### **A1** - Measured data of the scope for 8 bit vs 10 bit mode from 0 Hz to 120 MHz

This 10 bit mode as a big attenuation up until the -3dB mark, it's not a very flat curve. This was the main motivation to start this project. <br>
<br>
So I took the following measurements of **1 Vpp** at **8 bits** and at **10 bits**: <br>
**10MHz**  8: 1.027V – 10: 1.0067V -> delta:  **20.3mV** <br>
20MHz   8: 1.027V – 10: 1.000V -> delta:  27mV <br>
30MHz  8: 1.031V – 10: 990mV -> delta:  41mV <br>
40MHz  8: 1.033V – 10: 974mV -> delta:  59mV <br>
**50MHz** 8: 1.030V – 10: 948mV -> delta:  **82mV** <br>
60MHz  8: 1.031V – 10: 921mV -> delta:  110mV <br>
70MHz  8: 1.032V – 10: 889mV -> delta:  143mV <br>
80MHz  8: 1.028V – 10: 850mV -> delta:  178mV <br>
90MHz  8: 1.029V – 10: 812mV -> delta:  217mV <br>
**100MHz**  8: 1.025V – 10: 770mV -> delta: **255mV** <br>
110MHz  8: 1.032V – 10: 732mV -> delta:  300mV <br>
120MHz  8: 1.030V – 10: 677mV  -> delta:  353mV <br>

### **A2** - Measured data for 20 MHz bandwidth limit 8 bit mode from 0 Hz to 40 MHz

Data points png with graphs of attenuation and phase-shift. <br>
![Attenuation image](./Siglent_SDS2104_Plus/Data_collected/Charact_freq_response_ampl_phase_shift_20MHz_bandwidth_limited.png) <br>
<br>
The excel file is:<br>
[Attenuation excel file](./Siglent_SDS2104_Plus/Data_collected/Osciloscope_20MHz_bandwidth_limit_v04.xlsx) <br>

### **A3** - Program that extracts the attenuation data points of an FFT graph 

I made **a program to extract with some degree of precision the attenuation characterization data points, of an FFT graph image posted on the EEVBlog forum. It was made width a RF Signal Generator from 0 Hz to 1 GHz.** I generated a CSV with the directly obtained data points. I also used an interpolation algorithm to generate, the in between points in **dBV** and calculate the **Volts scale factor** for each frequency. I Generated a CSV from 0 Hz to 1 GHz in 10 MHz and 1 MHz steps. The validation, that the data was extracted correctly came from the 4 data points that are in the image and they had a **very small error, for example the 570 MHz in the image, as numerical value written -2.99dB and the point interpolated as a value of -2.9725 dB.** Note that this point nor it's neighbors aren't even directly accessible from the FFT plot, because the markers are large in with and they are in front, so this points had to be interpolated. <br> 
<br>
See in the EEVBlog forum, the EEVBlog thread for this project **Oscilloscope frequency response correction program** in the beginning of this document. <br> 
<br>
Following is the validation ... <br>
**Input image:** "SDS2354Xplus_2GSa_8bit_1GHz.png" <br>
**Source of image:** The post on EEVBlog Forum from the member **Performa01** on the topic "Siglent SDS2000X Plus coming", inside the area "Test Equipment".<br>
[Performa01 post](https://www.eevblog.com/forum/testgear/siglent-sds2000x-plus-coming/msg2787168/#msg2787168) <br>
<br>
The FFT input image that we will extract the data. <br>
![The FFT input image that we will extract the data](./Siglent_SDS2104_Plus/Extract_attenuation_values_from_scope_FFT_image/img_in/SDS2354Xplus_2GSa_8bit_1GHz.png)<br>
<br>
Data interpolated from the extracted FFT input image. <br>
![Program output image](./Siglent_SDS2104_Plus/Extract_attenuation_values_from_scope_FFT_image/output_example_of_interpolated_values_that_exist_in_the_image.png) <br>
<br>
FFT output image with extracted data points supper imposed. Note: When there were more then one vertical plot data pixel I average the position to the vertical middle of the blob.<br>
![FFT validation output image](./Siglent_SDS2104_Plus/Extract_attenuation_values_from_scope_FFT_image/output_out/output_debug_img.png) <br>
<br>
This program **code** is in [Siglent_SDS2104_Plus directory](./Siglent_SDS2104_Plus/Extract_attenuation_values_from_scope_FFT_image/) <br>
<br>
The **main program file** is [extract_attenuation_values_from_scope_fft_image.py](./Siglent_SDS2104_Plus/Extract_attenuation_values_from_scope_FFT_image/extract_attenuation_values_from_scope_fft_image.py) <br>
<br>
The CSV data files extracted are: <br>
[dbVAttenuationTable_OriginalFreq_0_to_1_GHz.csv](./Siglent_SDS2104_Plus/Extract_attenuation_values_from_scope_FFT_image/output_out/dbVAttenuationTable_OriginalFreq_0_to_1_GHz.csv) <br>
[dbVAttenuationTable_interpol_10M_step_0_to_1_GHz.csv](./Siglent_SDS2104_Plus/Extract_attenuation_values_from_scope_FFT_image/output_out/dbVAttenuationTable_interpol_10M_step_0_to_1_GHz.csv) <br>
[dbVAttenuationTable_interpol_1M_step_0_to_1_GHz.csv](./Siglent_SDS2104_Plus//Extract_attenuation_values_from_scope_FFT_image/output_out/dbVAttenuationTable_interpol_1M_step_0_to_1_GHz.csv) <br>


## **B** - Rigol DS1104Z .... current progress

This code is under the directory. <br>
[Rigol_DS1104Z directory](./Rigol_DS1104Z/) <br>
<br>
1. ....

2. ....

## License
MIT Open Source license.

## Have fun!
Best regards, <br>
Joao Nuno Carvalho <br>