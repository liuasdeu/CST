from miditoolkit import MidiFile
import os
import sys
import miditoolkit
import numpy as np
import matplotlib.pyplot as plt

def get_iois_count(x):
    cnt = [0] * (103)
    for iois in x:
        if iois != 0:
            cnt[iois] += 1
    return np.array(cnt)

def print_max_number(arr):
    if not arr:
        print("数组为空")
        return

    max_num = arr[0]

    for num in arr:
        if num > max_num:
            max_num = num

    print("最大数字为:", max_num)

def cal_overlap(gt_d, hyp_d):
    sum_gt = np.sum(gt_d) if np.sum(gt_d) > 0 else 1
    sum_hyp = np.sum(hyp_d) if np.sum(hyp_d) > 0 else 1
    gt_d = gt_d.astype(np.float32) / sum_gt
    hyp_d = hyp_d.astype(np.float32) / sum_hyp
    diff = np.abs(gt_d - hyp_d)
    overlap = (gt_d + hyp_d - diff) / 2
    return np.sum(overlap)

if __name__ == '__main__':
    # assert len(sys.argv) == 1 + 2 +3 + 4
    hyp_prefix1 = sys.argv[1]
    hyp_prefix2 = sys.argv[2]
    hyp_prefix3 = sys.argv[3]
    gt_prefix = sys.argv[4]

    cnt1 = [0] * (103)
    cnt2 = [0] * (103)
    cnt3 = [0] * (103)
    cnt4 = [0] * (103)

    for filename in os.listdir(f'{hyp_prefix1}/'):
        hyp_midi1 = miditoolkit.MidiFile(f'{hyp_prefix1}/{filename}')
        iois_hyp1 = []
        prev_onset = None
        ticks_per_beat1 = hyp_midi1.ticks_per_beat
        # print(ticks_per_beat2)
        for track in hyp_midi1.instruments:
            for note in track.notes:
                if prev_onset is not None:
                    ioi_hyp1 = (note.start // 120) - prev_onset
                    iois_hyp1.append(ioi_hyp1)
                    prev_onset = note.start // 120
                else:
                    prev_onset = note.start // 120

            # print(track)
        # print(iois_hyp3)
        # print_max_number(iois_hyp3)
        cnt1 = cnt1 + get_iois_count(iois_hyp1)

    for filename in os.listdir(f'{hyp_prefix2}/'):
        hyp_midi2 = miditoolkit.MidiFile(f'{hyp_prefix2}/{filename}')
        iois_hyp2 = []
        prev_onset = None
        ticks_per_beat2 = hyp_midi2.ticks_per_beat
        # print(ticks_per_beat2)
        for track in hyp_midi2.instruments:
            for note in track.notes:
                if prev_onset is not None:
                    ioi_hyp2 = (note.start // 120) - prev_onset
                    iois_hyp2.append(ioi_hyp2)
                    prev_onset = note.start // 120
                else:
                    prev_onset = note.start // 120

            # print(track)
        # print(iois_hyp3)
        # print_max_number(iois_hyp3)
        cnt2 = cnt2 + get_iois_count(iois_hyp2)

    for filename in os.listdir(f'{hyp_prefix3}/'):
        hyp_midi3 = miditoolkit.MidiFile(f'{hyp_prefix3}/{filename}')
        iois_hyp3 = []
        prev_onset = None
        ticks_per_beat3 = hyp_midi3.ticks_per_beat
        # print(ticks_per_beat3)   480
        for track in hyp_midi3.instruments:
            for note in track.notes:
                if prev_onset is not None:
                    ioi_hyp3 = (note.start // 120) - prev_onset
                    iois_hyp3.append(ioi_hyp3)
                    prev_onset = note.start // 120
                else:
                    prev_onset = note.start // 120

            # print(track)
        # print(iois_hyp3)
        # print_max_number(iois_hyp3)
        cnt3 = cnt3 + get_iois_count(iois_hyp3)

    for filename in os.listdir(f'{gt_prefix}/'):
        gt_midi = miditoolkit.MidiFile(f'{gt_prefix}/{filename}')
        iois_gt = []
        prev_onset = None
        ticks_per_beat_gt = gt_midi.ticks_per_beat
        # ticks_per_sixteenth_note = ticks_per_beat //4
        # tempo = gt_midi.tempo_changes[0].tempo
        # print(ticks_per_beat_gt)  220
        for track in gt_midi.instruments:
            for note in track.notes:
                if prev_onset is not None:
                    ioi_gt = (note.start // 55) - prev_onset
                    iois_gt.append(ioi_gt)
                    prev_onset = note.start // 55
                else:
                    prev_onset = note.start // 55
        # print_max_number(iois_gt)
        cnt4 = cnt4 + get_iois_count(iois_gt)
    # print(cnt4)

    array1 = cnt1
    array2 = cnt2
    array3 = cnt3
    array4 = cnt4

    print(cal_overlap(array4, array1))
    print(cal_overlap(array4, array2))
    print(cal_overlap(array4, array3))

    array1 = array1 / np.sum(array1)
    array2 = array2 / np.sum(array2)
    array3 = array3 / np.sum(array3)
    array4 = array4 / np.sum(array4)

    def plot_multi_bar_chart(data_list):
        num_bars = len(data_list[0])  # 假设每个一维列表的长度相同
        num_datasets = len(data_list)

        bar_width = 0.2
        bar_positions = np.arange(num_bars)

        for i, data in enumerate(data_list):
            if i == 0:
                a = "telemelody_lmdmatched"
            if i == 1:
                a = "telemelody_lmdfull"
            if i == 2:
                a = "CST"
            if i == 3:
                a = "gruth"
            plt.bar(bar_positions + i * bar_width, data, width=bar_width, label=a)


        plt.xlabel('Notes inter-onset-interval')
        plt.ylabel('Count (normalized)')
        # plt.title('Comparison of Note inter-onset-interval')
        plt.xticks(bar_positions + (num_datasets - 1) * bar_width / 2, [j * 0.25 for j in range(num_bars)])
        plt.legend()

        plt.show()


    # 你的输入数据，每个列表代表一个数据集
    dataset1 = array1
    dataset2 = array2
    dataset3 = array3
    dataset4 = array4

    # 将数据组成列表传入函数
    plot_multi_bar_chart([dataset1, dataset2, dataset3, dataset4])