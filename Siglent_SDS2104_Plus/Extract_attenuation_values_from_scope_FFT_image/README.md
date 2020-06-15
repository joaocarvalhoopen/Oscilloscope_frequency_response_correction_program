# Oscilloscope frequency response correction program 
This is a program to try make "many scope" give a more real representation of the signal. 

## Description
This is a project to correct (equalize) the scope frequency response of "any scope" in a PC program. <br>
When it is done (this project is on going), it will make a frequency domain equalization that will correct the scopes model specific frequency response, the amplitude attenuation and the phase-shift for each frequency that the input signal is composed, then it will reconstruct the time domain signal so that it can be visualized, analyzes and uploaded to the scope REF_A channel for direct comparison. <br>
This is nothing new, a similar equalization is made is MIMO WiFi Routers and 5G, one of it's implementation is called SC-FME (Single Carrier - Frequency Domain Equalization).

## See this project **EEVBlog thread** where many of the concepts that will be used are heavily detailed  

I put it under **Test Equipment**.<br>
Topic: **Oscilloscope frequency response correction program** <br>
[https://www.eevblog.com/forum/testgear/oscilloscope-frequency-response-correction-program/](https://www.eevblog.com/forum/testgear/oscilloscope-frequency-response-correction-program/) <br>

## Components that influence a scope frequency response
-Scope probe frequency response or cable connected.
-Input impedance selected (1 M Ohm or 50 Ohms)
-Scope low noise amplifier frequency response in the front end.
-Anti-aliasing filter before the input of the sampling ADC.
-ADC (Analog to Digital Converter) sampling rate and general characteristics.
<br>
All those factor contribute to the frequency response of a scope. But they can be measure, and inverted by applying **FDE - Frequency Domain Equalization**.  

## Steps needed

1. For a given model, obtain the scope frequency response characterization from 0 Hz to half the ADC sampling frequency. This in terms of amplitude attenuation and phase-shift characterization for each frequency, ideally a sweep, but can also be in steps.
2. Automate the tests (Optionally). 
3. The program connects to the scope by PyVisa library.
4. The processing will be.
   1. Read the buffer from the scope
   2. Do an FFT(signal), Fast Fourier Transform on the signal and transform it from the time domain into the frequency domain.
   3. In the frequency domain, apply to each frequency the correction in terms of attenuation and phase-shift (the inverse).
   4. Do an iFFT( ), inverse Fast Fourier Transform on the signal and reconstruct the original signal more accurately.
   5. Show it on the PC in a graph plot.
5. Send it to the scope REF_A channel for comparison. 

## Oscilloscopes targeted
In principal the same method could be applied to any scope brand or model.

### Siglent SDS2104-Plus 100 MHz for up to 945 MHz equalization
The first scope model that the software will be targeting is the 100 MHz Siglent SDS2104-Plus 2GSa 8bit with a small hack to 570 MHz -3dB bandwidth. But that has a frontend that can show signals even at least at 945 MHz. If they are ony attenuated and phase sifted at each frequency, in principal they can be corrected and the signal reconstructed up to the max limit off in this case 945 MHz.

### Rigol DS1104Z 100 MHz for maybe up 300 MHz to 400 MHz equalization
This will be the second scope targeted by this program.

### Siglent SDS1104X-E
This will possibly be the third scope targeted by this program.

### Other possible scopes targeted by the program directly by me
- Rigol DS1052E 50 MHz
- Hantek 100 MHz 


# Current progress....

## Siglent SDS2104-Plus .... current progress

This code is under the directory. <br>
[Siglent_SDS2104_Plus directory](.\\Siglent_SDS2104_Plus directory\\) <br>

1. I made **a program to extract with some degree of precision the attenuation characterization data points of an FFT graph image posted on the EEVBlog forum that was made width a RF Signal Generator from 0 Hz to 1 GHz.** I generated a CSV with the directly obtained data points and I also used a interpolation algorithm to generate the in between points in dBV and generate the Volts scale factor for each frequency. I Generated a CSV from 0 Hz to 1 GHz in 10 MHz and 1 MHz steps. The validation that the data was correctly being taken come from the 4 points that are in the image and that have a **very small error, for example the 570 MHz in the image as numerical value written -2.99dB and the point interpolated as a value of -2.9725 dB.** Note that this point isn't even directly accessible from the FFT plot because the markers are large in with and they are in from, so this points had to be interpolated. See the EEVBlog the following EEVBlog post on the EEVBlog thread for this project **Oscilloscope frequency response correction program** in the beginning of this document. The code is [Siglent_SDS2104_Plus directory](.\\Siglent_SDS2104_Plus\\extract_attenuation_values_from_scope_fft_image\\)

## Rigol DS1104Z .... current progress

1. ....

2. ....

## License
MIT Open Source license.

## Have fun!
Best regards, <br>
Joao Nuno Carvalho <br>