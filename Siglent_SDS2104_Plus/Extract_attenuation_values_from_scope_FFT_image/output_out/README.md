# Description

For the scope Siglent SDS2000X Plus, regarding this thread project, I made an open source Python program to extract an amplitude attenuation CSV table file with all the data points from the PNG image of the FFT attenuation plot. The scope  **screenshoot was taken by EEVBlog member  Performa01** with an RF Signal Generator, and I think that it is a very accurate signal generator. <br>
<br>
The image was posted here: <br>
[https://www.eevblog.com/forum/testgear/siglent-sds2000x-plus-coming/msg2787168/#msg2787168](https://www.eevblog.com/forum/testgear/siglent-sds2000x-plus-coming/msg2787168/#msg2787168) <br>
<br> 
The program extraction is also very accurate, I explain it and show exactly that, in the github page of the project:<br>
[https://github.com/joaocarvalhoopen/Oscilloscope_frequency_response_correction_program](https://github.com/joaocarvalhoopen/Oscilloscope_frequency_response_correction_program)<br>
<br>
It uses interpolation to get the “Inter-pixel” point value and I extracted 3 table CSV files. <br>
-Attenuation data extracted directly from the image with the range 0 Hz to 1 GHz (**no interpolation**).<br>
-Attenuation data interpolated from **0 Hz to 1 GHz in 10 MHz steps.** <br>
-Attenuation data interpolated from **0 Hz to 1 GHz in  1MHz steps.** <br>
<br>
For example for the 570 MHz with  -2.99 dBV mark . The data isn´t even on the image plot line because the wide marker is over it, but I have extracted automatically all the points including the point to the left and to the right of the marker and the result was: <br>
<br>
| Type of measurement                                     | Frequency | Attenuation   |
|---------------------------------------------------------|-----------|---------------|
|**Measured by the scope** in text in the image           |**570 MHz**|  **-2.99 dBV**|
|**Extracted from pixels** and interpolated by my program |**570 MHz**|**-2.9725 dBV**|
|**Error**                                                |           | **0.0275 dBV**|
<br>
The program work by searching a list of zones, in this case only two zones were needed to extract all the points. <br>
<br>
Feel free to use it to extract other FFT plots for the Siglent, the license is MIT open source license. <br>

The **Python code file** is this:
[https://github.com/joaocarvalhoopen/Oscilloscope_frequency_response_correction_program/blob/master/Siglent_SDS2104_Plus/Extract_attenuation_values_from_scope_FFT_image/extract_attenuation_values_from_scope_fft_image.py](https://github.com/joaocarvalhoopen/Oscilloscope_frequency_response_correction_program/blob/master/Siglent_SDS2104_Plus/Extract_attenuation_values_from_scope_FFT_image/extract_attenuation_values_from_scope_fft_image.py) <br>

**EEVBlog Post for discussion** of this topics: <br>
[https://www.eevblog.com/forum/testgear/oscilloscope-frequency-response-correction-program/msg3097328/#msg3097328](https://www.eevblog.com/forum/testgear/oscilloscope-frequency-response-correction-program/msg3097328/#msg3097328) <br>
<br>
Best regards, <br>
João Nuno Carvalho <br>
<br>
