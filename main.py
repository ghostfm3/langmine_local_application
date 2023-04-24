import PySimpleGUI as sg
import os
from collections import Counter
from count import janome_token, plt_counter, remove_stop_word, wordcloud_result, sentiment_analysis, draw_graph, label_list

def draw_img(image_path, drow_name):
    image_folder_path = image_path # 画像フォルダのパスを設定する
    image_filenames = os.listdir(image_folder_path) # 画像フォルダ内のファイル名を取得する
    image_filenames = [filename for filename in image_filenames if filename.endswith('.png')] # pngファイルのみを取得する
    if len(image_filenames) > 0:
        image_filename = os.path.join(image_folder_path, image_filenames[0]) # 最初の画像ファイルを取得する
        image_layout = [[sg.Image(filename=image_filename)]] # 画像を表示するレイアウトを作成する
        image_window = sg.Window(drow_name, image_layout) # 画像を表示する新しいウィンドウを生成する
        image_event, image_values = image_window.read() # 画像ウィンドウのイベントループを開始する
        image_window.close() # 画像ウィンドウを閉じる

sg.theme('DarkAmber')   # デザインテーマの設定

# ウィンドウに配置するコンポーネント
layout = [  [sg.Text('PreLangMine')],
            [sg.Text('File', size=(15, 1)), sg.Input(), sg.FileBrowse('Upload File', key='inputFilePath')],
            # [sg.Text('Remove rubi', size=(15, 1)),sg.Combo(('ON', 'OFF'), default_value="ON",size=(10, 1), key='lattice')],
            [sg.Button('Frequency'), sg.Button('WordCloud'), sg.Button('EmotionRate')],
            [sg.Button('Exit')]]

# ウィンドウの生成
window = sg.Window('PreLangMine', layout)

# イベントループ
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break

    if event == 'Frequency':
        basename_without_ext = os.path.splitext(os.path.basename(values['inputFilePath']))[0] 
        filename = "./input_file/" + basename_without_ext +".txt"
        word_list = janome_token(filename)
        plt_counter(Counter(word_list))
        draw_img("./output/freq",'Frequency Image')   
    elif event == 'WordCloud':
        basename_without_ext = os.path.splitext(os.path.basename(values['inputFilePath']))[0] 
        filename = "./input_file/" + basename_without_ext +".txt"
        word_list = janome_token(filename)
        stop_word = ['こと', 'よう', 'そう', 'これ', 'それ', 'あれ', 'どれ', 'の', 'ん', 'ぼく', 
        'もの','もち','等', '二','三', '十', '中', 'ひと', 'きみ', '人', '方', 'たち','一','どこ', 'つて', 'やう', 'うし']
        word_list = remove_stop_word(word_list, stop_word)
        text2 = ' '.join(word_list)
        wordcloud_result('white','./font/ipaexm.ttf',500,400,text2)
        draw_img("./output/wordcloud",'WordCloud Image')
    elif event == 'EmotionRate':
        basename_without_ext = os.path.splitext(os.path.basename(values['inputFilePath']))[0] 
        filename = "./input_file/" + basename_without_ext +".txt"
        with open(filename, 'r', encoding='utf-8') as f:
            text = f.read()  # ファイルからテキストを読み込み
        
        sentences = text.split('。')  # 句点で文章を分割
        sentences = [s.strip() + '。' for s in sentences if s.strip()]  # 文章を配列に格納
        
        count_1, r_dict = sentiment_analysis(sentences)
  
    
        d = {label: count for label, count in zip(label_list, count_1) if count != 0}
        draw_graph(d)
        draw_img("./output/emotion",'Emotion Rate Image')

window.close()