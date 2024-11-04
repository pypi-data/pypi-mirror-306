#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   mne 
@Time        :   2024/10/15 17:19
@Author      :   Xuesong Chen
@Description :   
"""

import mne
import re
import numpy as np

from wuji.Reader.EDF.Base import EDFHeaderParser


class MNEReader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.header = None
        self._parse_file()

    def _parse_file(self):
        self.header = EDFHeaderParser(self.file_path)
        self.signal_labels = self.header.get_signal_labels()
        self.duration = self.header.get_duration()
        self.start_recording_time = self.header.get_recording_start_time()
        self._assign_signal_types()

    def _assign_signal_types(self):
        self.signal_type = []
        for idx, sig in enumerate(self.signal_labels):
            if re.search('E[CK]G', sig, re.IGNORECASE):
                self.signal_type.append('ecg')
            elif re.search('S[pa]O2', sig, re.IGNORECASE):
                self.signal_type.append('spo2')
            elif re.search('ABD', sig, re.IGNORECASE):
                self.signal_type.append('abd')
            elif re.search('CHEST|THO', sig, re.IGNORECASE):
                self.signal_type.append('chest')
            elif re.search('C3-M2|C4-M1|F3-M2|F4-M1|O1-M2|O2-M1|C3|C4|F3|F4|O1|O2', sig, re.IGNORECASE):
                self.signal_type.append('eeg')
            elif re.search('EMG', sig, re.IGNORECASE):
                self.signal_type.append('emg')
            elif re.search('EOG', sig, re.IGNORECASE):
                self.signal_type.append('eog')
            elif re.search('Snore', sig, re.IGNORECASE):
                self.signal_type.append('snore')
            elif re.search('position', sig, re.IGNORECASE):
                self.signal_type.append('position')
            elif re.search('AirFlow', sig, re.IGNORECASE):
                self.signal_type.append('nasal_thermometer')
            elif re.search('CFLOW|Pressure', sig, re.IGNORECASE):
                self.signal_type.append('nasal_pressure')
            elif re.search('Flow|NEW AIR', sig, re.IGNORECASE):
                self.signal_type.append('flow')
            elif re.search('Numeric Aux', sig, re.IGNORECASE):
                self.signal_type.append('trigger')
            elif re.search('Pleth', sig, re.IGNORECASE):
                self.signal_type.append('ppg')
            else:
                self.signal_type.append('unk')
        self.signal_type = np.array(self.signal_type, dtype='U20')

    def get_start_recording_time(self):
        return self.start_recording_time

    def get_number_of_signals(self, type='ecg'):
        return np.sum(self.signal_type == type)

    def get_channel_name(self, type='ecg', order=None):
        if order is None:
            return self.signal_labels[self.signal_type == type]
        else:
            return self.signal_labels[self.signal_type == type][order]

    def get_signal(self, ch_name=None, type='ecg', tmin=None, tmax=None, order=0):
        '''
        获取所有匹配信号，order代表次序，0代表第一个匹配的信号
        :param ch_name:
        :param type:
        :param tmin:
        :param tmax:
        :param order:
        :return:
        '''
        if ch_name:
            idx = np.argwhere(self.signal_labels == ch_name).flatten()[order]
        else:
            idx = np.argwhere(self.signal_type == type).flatten()[order]
        ch_name = self.signal_labels[idx]
        n_same_same_ch_before = np.sum(self.signal_labels[:idx] == ch_name)
        tmp_raw = mne.io.read_raw_edf(self.file_path, include=ch_name)
        unit = tmp_raw.info['chs'][n_same_same_ch_before]['unit']
        # 107 : 'FIFF_UNIT_V'
        assert unit == 107, f"Unit of {ch_name} is not FIFF_UNIT_V"
        scale_map = {
            'ecg': 1e6, # V -> mV
            'eeg': 1e6, # V -> uV
        }
        scale = scale_map.get(type, 1e6)
        if tmin is None or tmax is None:
            data = tmp_raw.get_data()[n_same_same_ch_before] * scale
        else:
            data = tmp_raw.get_data(tmin=tmin, tmax=tmax)[n_same_same_ch_before] * scale
        tmp_raw.close()
        return data

    def get_sample_frequency(self, ch_name=None, type='ecg', order=0):
        if ch_name:
            idx = np.argwhere(self.signal_labels == ch_name).flatten()[order]
        else:
            idx = np.argwhere(self.signal_type == type).flatten()[order]
        ch_name = self.signal_labels[idx]
        tmp_raw = mne.io.read_raw_edf(self.file_path, include=[ch_name])
        fs = int(tmp_raw.info['sfreq'])
        tmp_raw.close()
        return fs

    def get_channel(self, ch_name=None, type=None, tmin=None, tmax=None, order=0):
        """
        获取信号和采样率，order代表次序，0代表第一个匹配的信号
        """
        signal = self.get_signal(ch_name, type, tmin, tmax, order)
        sampling_rate = self.get_sample_frequency(ch_name, type, order)
        return signal, sampling_rate

    def get_duration(self):
        return self.duration


if __name__ == '__main__':
    from wuji.Reader import NSRREDFReader
    fp = '/Users/cxs/Downloads/scored studies/00000835-113072/00000835-113072_4587577.edf'
    fp = '/Users/cxs/Downloads/chat-baseline-300641.edf'
    from pyedflib.highlevel import read_edf_header
    header = read_edf_header(fp)
    import pyedflib
    import neurokit2 as nk
    # header = pyedflib.highlevel.read_edf_header(fp)
    reader = NSRREDFReader(fp)
    mne_reader = MNEReader(fp)
    # print(reader.signal_labels)
    print(mne_reader.signal_labels)
    sig = reader.get_signal(type='ecg', tmin=None, tmax=3600+300)
    pyedflib_fs = reader.get_sample_frequency(type='ecg')
    sig2 = mne_reader.get_signal(type='ecg', tmin=None, tmax=3600+300)
    import matplotlib.pyplot as plt
    plt.plot(nk.ecg_clean(sig, sampling_rate=pyedflib_fs), label='reader')
    # plt.plot(nk.signal_resample(sig2, desired_length=len(sig2) // 5), label='mne_reader')
    plt.legend()
    plt.show()
    print(reader.signal_labels)
