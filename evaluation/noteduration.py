import numpy as np
import os
import sys
import miditoolkit
import matplotlib.pyplot as plt

ALIGN = '[align]'
SEP = '[sep]'
# Duration_vocab 字典将 MIDI 中的时长（以 tick 为单位）映射为整数，每个整数表示该时长的百分之一，取值范围为 0.25~33.00 秒。
# list(range(25, 3325, 25)) 生成一个从 25 到 3325 的整数列表（132），步长为 25，表示 MIDI 中的时长（以 tick 为单位）
Duration_vocab = dict([(129+i, x/100)
                       for i, x in enumerate(list(range(25, 3325, 25)))])
Duration_vocab_re = dict([(x/100, 129+i)
                          for i, x in enumerate(list(range(25, 3325, 25)))])
MAX_DUR = int(max(Duration_vocab.keys()))
REST = 128


def get_pitch_count(x):
    cnt = [0] * (128 + 1)
    for pitch in x:
        if pitch != 128:
            cnt[pitch] += 1
    return np.array(cnt)

def get_dur_count(x):
    cnt = [0 for i, x in enumerate(list(range(25, 3325, 25)))]
    min_dur = Duration_vocab[min(x)]
    for dur in x:
        cur_dur = Duration_vocab[dur]
        cur_idx = int(cur_dur / min_dur)
        if cur_idx < len(cnt):
            cnt[cur_idx] += 1
        else:
            cnt[-1] += 1
    return np.array(cnt)


def separate(string, use_word=False):
    if not use_word:
        tmp = [i for i in string.strip().split() if i not in [SEP, ALIGN]]
        pitch = []
        dur = []
        for i in range(0, len(tmp), 2):
            pitch.append(int(tmp[i]))
            dur.append(int(tmp[i+1]))
        return pitch, dur
    else:
        tmp = [i for i in string.strip().split() if i not in [SEP]]
        p = []
        d = []
        is_pitch = True
        cur_dur = 0
        for idx in range(len(tmp)):
            if tmp[idx] != ALIGN:
                if is_pitch:
                    p.append(int(tmp[idx]))
                else:
                    cur_dur += Duration_vocab[int(tmp[idx])]
                is_pitch = not is_pitch
            else:
                if cur_dur in Duration_vocab_re:
                    d.append(Duration_vocab_re[cur_dur])
                cur_dur = 0
        if cur_dur > 0 and cur_dur in Duration_vocab_re:
            d.append(Duration_vocab_re[cur_dur])
        return p, d


def get_melody(mid_obj):
    def get_vocab(dur):
        beat = dur // (ticks // 4)
        if beat == 0:
            beat = 1
        beat = beat / 4
        return str(Duration_vocab_re.get(beat, MAX_DUR))

    lyrics = mid_obj.lyrics
    notes = mid_obj.instruments[0].notes
    last_end = notes[0].start
    cur_melody = []
    ticks = mid_obj.ticks_per_beat
    max_lyric = len(lyrics)
    lyric_id = 1
    for note in notes:
        if lyric_id < max_lyric and lyrics[lyric_id].time == note.start:
            cur_melody.append(ALIGN)
            lyric_id += 1
        if note.start != last_end:
            cur_melody.append(str(128))
            cur_melody.append(get_vocab(note.start - last_end))
        cur_melody.append(str(note.pitch))
        cur_melody.append(get_vocab(note.end - note.start))
        last_end = note.end

    cur_melody.append(ALIGN)
    cur_melody.append(SEP)
    new_meldoy = []
    cur_pitch = []
    for i in cur_melody:
        if i == SEP:
            new_meldoy.append(i)
        elif i != ALIGN:
            new_meldoy.append(i)
            if int(i) < 128:
                cur_pitch.append(i)
        elif i == ALIGN:
            if len(cur_pitch):
                new_meldoy.append(i)
            cur_pitch = []
    cur_melody = new_meldoy

    return ' '.join(cur_melody)


def cal_overlap(gt_d, hyp_d):
    sum_gt = np.sum(gt_d) if np.sum(gt_d) > 0 else 1
    sum_hyp = np.sum(hyp_d) if np.sum(hyp_d) > 0 else 1
    gt_d = gt_d.astype(np.float32) / sum_gt
    hyp_d = hyp_d.astype(np.float32) / sum_hyp
    diff = np.abs(gt_d - hyp_d)
    overlap = (gt_d + hyp_d - diff) / 2
    return np.sum(overlap)


if __name__ == '__main__':
    # assert len(sys.argv) == 1 + 2
    # gt_prefix = sys.argv[2]

    hyp_prefix = sys.argv[1]
    hyp_prefix2 = sys.argv[2]
    hyp_prefix3 = sys.argv[3]
    hyp_prefix4 = sys.argv[4]

    pitch_overlap1 = [0] * 129
    dur_overlap1 = [0] * 132
    pitch_overlap2 = [0] * 129
    dur_overlap2 = [0] * 132
    pitch_overlap3 = [0] * 129
    dur_overlap3 = [0] * 132
    pitch_overlap4 = [0] * 129
    dur_overlap4 = [0] * 132
    # print(f'hyp: {hyp_prefix}   gt: {gt_prefix}')
    # print(os.listdir(f'{hyp_prefix}/'))
    for filename in os.listdir(f'{hyp_prefix}/'):
        hyp_midi = miditoolkit.MidiFile(f'{hyp_prefix}/{filename}')
        hyp = get_melody(hyp_midi)
        # gt_midi = miditoolkit.MidiFile(f'{gt_prefix}/{filename}')
        # gt = get_melody(gt_midi)
        hyp_pitch, hyp_dur = separate(hyp)
        # gt_pitch, gt_dur = separate(gt)
        pitch = get_pitch_count(hyp_pitch)
        duration = get_dur_count(hyp_dur)
        pitch_overlap1 = pitch_overlap1 + pitch
        dur_overlap1 = dur_overlap1 + duration
    for filename in os.listdir(f'{hyp_prefix2}/'):
        hyp_midi2 = miditoolkit.MidiFile(f'{hyp_prefix2}/{filename}')
        hyp2 = get_melody(hyp_midi2)
        # gt_midi = miditoolkit.MidiFile(f'{gt_prefix}/{filename}')
        # gt = get_melody(gt_midi)
        hyp_pitch2, hyp_dur2 = separate(hyp2)
        # gt_pitch, gt_dur = separate(gt)
        pitch2 = get_pitch_count(hyp_pitch2)
        duration2 = get_dur_count(hyp_dur2)
        pitch_overlap2 = pitch_overlap2 + pitch2
        dur_overlap2 = dur_overlap2 + duration2
    for filename in os.listdir(f'{hyp_prefix3}/'):
        hyp_midi3 = miditoolkit.MidiFile(f'{hyp_prefix3}/{filename}')
        hyp3 = get_melody(hyp_midi3)
        # gt_midi = miditoolkit.MidiFile(f'{gt_prefix}/{filename}')
        # gt = get_melody(gt_midi)
        hyp_pitch3, hyp_dur3 = separate(hyp3)
        # gt_pitch, gt_dur = separate(gt)
        pitch3 = get_pitch_count(hyp_pitch3)
        duration3 = get_dur_count(hyp_dur3)
        pitch_overlap3 = pitch_overlap3 + pitch3
        dur_overlap3 = dur_overlap3 + duration3
    for filename in os.listdir(f'{hyp_prefix4}/'):
        hyp_midi4 = miditoolkit.MidiFile(f'{hyp_prefix4}/{filename}')
        hyp4 = get_melody(hyp_midi4)
        # gt_midi = miditoolkit.MidiFile(f'{gt_prefix}/{filename}')
        # gt = get_melody(gt_midi)
        hyp_pitch4, hyp_dur4 = separate(hyp4)
        # gt_pitch, gt_dur = separate(gt)
        pitch4 = get_pitch_count(hyp_pitch4)
        duration4 = get_dur_count(hyp_dur4)
        pitch_overlap4 = pitch_overlap4 + pitch4
        dur_overlap4 = dur_overlap4 + duration4
    # 三个示例数组
    # array1 = pitch_overlap1
    # array2 = pitch_overlap2
    # array3 = pitch_overlap3
    array1 = dur_overlap1
    array2 = dur_overlap2
    array3 = dur_overlap3
    array4 = dur_overlap4

    array1 = array1 / np.sum(array1)
    array2 = array2 / np.sum(array2)
    array3 = array3 / np.sum(array3)
    array4 = array4 / np.sum(array4)
    print(cal_overlap(array4,array1))
    print(cal_overlap(array4,array2))
    print(cal_overlap(array4,array3))

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

        plt.xlabel('Note duration')
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


