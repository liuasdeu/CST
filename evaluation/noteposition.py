import numpy as np
import os
import sys
import miditoolkit
import matplotlib.pyplot as plt

ALIGN = '[align]'
SEP = '[sep]'
# Duration_vocab 字典将 MIDI 中的时长（以 tick 为单位）映射为整数，每个整数表示该时长的百分之一，取值范围为 0.25~33.00 秒。
# list(range(25, 3325, 25)) 生成一个从 25 到 3325 的整数列表（132），步长为 25，表示 MIDI 中的时长（以 tick 为单位）
Duration_vocab = dict([(129 + i, x / 100)
                       for i, x in enumerate(list(range(25, 3325, 25)))])
Duration_vocab_re = dict([(x / 100, 129 + i)
                          for i, x in enumerate(list(range(25, 3325, 25)))])
MAX_DUR = int(max(Duration_vocab.keys()))
REST = 128

# def get_melody_1(mid_obj):
#     notes = sorted(mid_obj.instruments[0].notes, key=lambda x: x.start)
#     positions = [0] * 16
#
#     prev_end = 0
#     for note in notes:
#         pos = note.start // 120
#         if pos == 0:
#             pos = 1
#         while pos > 16:
#             pos = pos - 16
#         if pos-1 == prev_end or pos -prev_end == -15:
#             positions[pos - 1] = positions[pos - 1] + 1
#         if pos-1 != prev_end and note.start//120 != 0:
#             if prev_end != 16:
#                 positions[prev_end] = positions[prev_end] + 1
#             else:
#                 positions[prev_end-1] = positions[prev_end-1] + 1
#         prev_end = note.end // 120
#         while prev_end > 16:
#             prev_end -= 16

    # return np.array(positions)

def get_melody_1(mid_obj):
    notes = sorted(mid_obj.instruments[0].notes, key=lambda x: x.start)
    positions = [0] * 16

    for note in notes:
        pos = note.start // 120
        if pos == 0:
            pos = 1
        while pos > 16:
            pos = pos - 16
        positions[pos - 1] = positions[pos - 1] + 1

    return np.array(positions)
def cal_overlap(gt_d, hyp_d):
    sum_gt = np.sum(gt_d) if np.sum(gt_d) > 0 else 1
    sum_hyp = np.sum(hyp_d) if np.sum(hyp_d) > 0 else 1
    gt_d = gt_d.astype(np.float32) / sum_gt
    hyp_d = hyp_d.astype(np.float32) / sum_hyp
    diff = np.abs(gt_d - hyp_d)
    overlap = (gt_d + hyp_d - diff) / 2
    return np.sum(overlap)


if __name__ == '__main__':

    hyp_prefix = sys.argv[1]
    hyp_prefix2 = sys.argv[2]
    hyp_prefix3 = sys.argv[3]
    hyp_prefix4 = sys.argv[4]


    hyp1_notepo = [0] * 16
    hyp2_notepo = [0] * 16
    hyp3_notepo = [0] * 16
    gt_notepo = [0] * 16

    for filename in os.listdir(f'{hyp_prefix}/'):
        hyp_midi = miditoolkit.MidiFile(f'{hyp_prefix}/{filename}')
        hyp_notepo1 = get_melody_1(hyp_midi)
        hyp1_notepo += hyp_notepo1


    for filename in os.listdir(f'{hyp_prefix2}/'):
        hyp_midi = miditoolkit.MidiFile(f'{hyp_prefix2}/{filename}')
        hyp_notepo2 = get_melody_1(hyp_midi)
        hyp2_notepo += hyp_notepo2
    for filename in os.listdir(f'{hyp_prefix3}/'):
        hyp_midi = miditoolkit.MidiFile(f'{hyp_prefix3}/{filename}')
        hyp_notepo3 = get_melody_1(hyp_midi)
        hyp3_notepo += hyp_notepo3
    for filename in os.listdir(f'{hyp_prefix4}/'):
        hyp_midi = miditoolkit.MidiFile(f'{hyp_prefix4}/{filename}')
        hyp_notepo4 = get_melody_1(hyp_midi)
        gt_notepo += hyp_notepo4


    array1 = hyp1_notepo
    array2 = hyp2_notepo
    array3 = hyp3_notepo
    array4 = gt_notepo

    # print(cal_overlap(array4,array1))
    # print(cal_overlap(array4,array2))
    # print(cal_overlap( array4,array3))

    array1 = array1 / np.sum(array1)
    array2 = array2 / np.sum(array2)
    array3 = array3 / np.sum(array3)
    array4 = array4 / np.sum(array4)

    print(cal_overlap(array4,array1))
    print(cal_overlap(array4,array2))
    print(cal_overlap( array4,array3))


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

        plt.xlabel('Note position in Bar')
        plt.ylabel('Count (normalized)')
        # plt.title('Comparison of Note Durations')
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

    # # 将数据组成列表传入函数
    # plot_multi_bar_chart([dataset1])

