# 《CST: A Melody Generation Method Based on Lyrics and Themes》
This new method generates melodies from lyrics, enhancing the quality of lyric-melody generation to address the following issues:
1. Lyrics usually need to be specified by the user in advance, greatly limiting user convenience.
2. The generated melodies often lack distinct structure, with the chorus, which is key to conveying musical emotion, often being neglected.
### 1. Environment Setup
Install the required packages:
<div style="background-color: #f1f1f1; padding: 10px; font-size: 1em;">
  <pre>
    <code>
      pip install -r requirements.txt
    </code>
  </pre>
</div>
The innovations proposed in this paper are implemented through a local installation of Fairseq. Therefore, it is recommended to proceed with the local installation of Fairseq:
<div style="background-color: #f1f1f1; padding: 10px; font-size: 1em;">
  <pre>
    <code>
    cd fairseq
    pip install –editable ./
    </code>
  </pre>
</div>
Fairseq can be downloaded from here.[Click here](https://drive.google.com/drive/folders/1of0Jdh0z3uALvSTtBUq6Ub5ulEnS5xkI?usp=drive_link)

### 2. Dataset Download
Navigate to the train/template2melody directory and download the lmd_full MIDI dataset into this folder:
<div style="background-color: #f1f1f1; padding: 10px; font-size: 1em;">
  <pre>
    <code>
     cd train/template2melody
    </code>
  </pre>
</div>

### 3. Data Preparation
Generate and align the data:
<div style="background-color: #f1f1f1; padding: 10px; font-size: 1em;">
  <pre>
    <code>
    cd train/template2melody
    python gen.py lmd_full lmd_full
    python gen_align.py lmd_full
    </code>
  </pre>
</div>
After this step, a data folder will appear in the train/template2melody directory.

### 4. Data Binarization
Convert the data to binary format:
<div style="background-color: #f1f1f1; padding: 10px; font-size: 1em;">
  <pre>
    <code>
    cd train/template2melody
    bash preprocess.sh lmd_full lmd_full
    </code>
  </pre>
</div>
After this step, a data-bin folder will appear in the train/template2melody directory.

### 5. Model Training
<div style="background-color: #f1f1f1; padding: 10px; font-size: 1em;">
  <pre>
    <code>
    cd train/template2melody
    bash train.sh lmd_full
    </code>
  </pre>
</div>
After this step, checkpoints and logs folders will appear in the train/template2melody directory. 

### 6. Theme-to-Melody
Navigate to the chat directory.
#### (1) Model Preparation
Save the checkpoints in checkpoints/{model_prefix}. This should include the Chinese and English models for lyrics-rhythm, and the template-melody model trained with our innovations. Save the dictionaries in data-bin/{model_prefix}. Dictionary data is provided in data-bin.
Download the model checkpoints here.[Click here](https://drive.google.com/drive/folders/1mNGQuINnx_GHHGd3vrjRZq8vNoxjgSif?usp=drive_link)
#### (2) Theme-to-Melody Generation
<div style="background-color: #f1f1f1; padding: 10px; font-size: 1em;">
  <pre>
    <code>
    cd chat
    python homepage.py
    </code>
  </pre>
</div>
After this step, a webpage will appear. Navigate to this page to enter the system, where you can request lyrics generation, followed by melody generation.

### 7. Lyric-to-Melody
Navigate to the inference directory.
#### (1) Data Preparation
Prepare word-level (EN) or character-level (ZH) lyrics in data/{lang}/{data_prefix}/lyrics.txt, and chord progressions in data/{lang}/{data_prefix}/chord.txt. For English lyrics, also prepare syllable-level lyrics in data/en/{data_prefix}/syllable.txt as input for the lyrics-rhythm model. Examples are provided in data/en/test/ and data/zh/test/.
#### (2) Model Preparation
Save the checkpoints in checkpoints/{model_prefix}, including the Chinese and English models for lyrics-rhythm and the template-melody model trained with our innovations. Save the dictionaries in data-bin/{model_prefix}. Dictionary data is provided in data-bin.
Download the model checkpoints here.[Click here](https://drive.google.com/drive/folders/1mNGQuINnx_GHHGd3vrjRZq8vNoxjgSif?usp=drive_link)
#### (3) Lyric-to-Melody Generation
<div style="background-color: #f1f1f1; padding: 10px; font-size: 1em;">
  <pre>
    <code>
    python infer_zh.py lyric2beat template2melody test zh
    python infer_en.py lyric2beat_en template2melody test en
    </code>
  </pre>
</div>
The first line generates melodies from Chinese lyrics, and the second line generates melodies from English lyrics. The generated melodies will be in the results/{lang}/ folder. We provide examples of lyric-to-melody.

### 8. Melody Evaluation
Navigate to the evaluation directory.
#### (1) Calculate similarity:
<div style="background-color: #f1f1f1; padding: 10px; font-size: 1em;">
  <pre>
    <code>
    cd evaluation
    python cal_similarity.py cst gruth
    </code>
  </pre>
</div>

#### (2) Calculate diversity:
<div style="background-color: #f1f1f1; padding: 10px; font-size: 1em;">
  <pre>
    <code>
    python cal_pitch_diversity.py cst gruth
    </code>
  </pre>
</div>

#### (3) Calculate inter-onset intervals (IOIs):
<div style="background-color: #f1f1f1; padding: 10px; font-size: 1em;">
  <pre>
    <code>
    python iois.py cst gruth
    </code>
  </pre>
</div>

