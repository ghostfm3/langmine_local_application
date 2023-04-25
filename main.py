import PySimpleGUI as sg
import os
import sys
from collections import Counter
from count import janome_token, plt_counter, remove_stop_word, wordcloud_result, sentiment_analysis, draw_graph, label_list

def delete_png_file(dir_path):
    '''
    フォルダ配下にファイルが存在するとき、ファイルを全て削除する。
    '''
    files = os.listdir(dir_path)
    if files:
        for file in files:
            os.remove(os.path.join(dir_path, file))

def text_statics(input_filename, event):
    '''
    イベント別テキスト処理
    '''
    filename = "./input_file/" + input_filename +".txt"
    word_list = janome_token(filename)

    if event == 'Frequency':
        return word_list
    elif event == 'WordCloud':
        stop_word = ['こと', 'よう', 'そう', 'これ', 'それ', 'あれ', 'どれ', 'の', 'ん', 'ぼく', 
        'もの','もち','等', '二','三', '十', '中', 'ひと', 'きみ', '人', '方', 'たち','一','どこ', 'つて', 'やう', 'うし']
        word_list = remove_stop_word(word_list, stop_word)
        text = ' '.join(word_list)
        return text 
    elif event == 'EmotionRate':
        with open(filename, 'r', encoding='utf-8') as f:
            text = f.read()      
        sentences = text.split('。')  # 句点で文章を分割
        sentences = [s.strip() + '。' for s in sentences if s.strip()]  # 文章を配列に格納    
        count_1, r_dict = sentiment_analysis(sentences)
        emotion_dict = {label: count for label, count in zip(label_list, count_1) if count != 0}
        return emotion_dict

def draw_img(image_path, drow_name):
    '''
    画像を読み込み別windowで出力する
    '''
    image_folder_path = image_path
    image_filenames = os.listdir(image_folder_path) 
    image_filenames = [filename for filename in image_filenames if filename.endswith('.png')]

    if len(image_filenames) > 0:
        image_filename = os.path.join(image_folder_path, image_filenames[0]) 
        image_layout = [[sg.Image(filename=image_filename)]] 
        image_window = sg.Window(drow_name, image_layout) 
        image_event, image_values = image_window.read() 
        image_window.close() 

def draw_page():
    # デザインテーマの設定
    sg.theme('DarkTeal7')   

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
            delete_png_file("./output/freq")
            delete_png_file("./output/wordcloud")
            delete_png_file("./output/emotion")
            break

        if event == 'Frequency':
            basename_without_ext = os.path.splitext(os.path.basename(values['inputFilePath']))[0] 
            try:
                word_list = text_statics(basename_without_ext,event)
            except FileNotFoundError:
                sg.popup("not exsit file")
                continue     
            plt_counter(Counter(word_list))
            draw_img("./output/freq",'Frequency Image')   
        elif event == 'WordCloud':
            basename_without_ext = os.path.splitext(os.path.basename(values['inputFilePath']))[0] 
            try:
                text2 = text_statics(basename_without_ext,event)
            except FileNotFoundError:
                sg.popup("not exsit file")
                continue   
            wordcloud_result('white','./font/ipaexm.ttf',500,400,text2)
            draw_img("./output/wordcloud",'WordCloud Image')
        elif event == 'EmotionRate':
            basename_without_ext = os.path.splitext(os.path.basename(values['inputFilePath']))[0] 
            try:
                emotion_dict = text_statics(basename_without_ext,event)
            except FileNotFoundError:
                sg.popup("not exsit file")
                continue   
            draw_graph(emotion_dict)
            draw_img("./output/emotion",'Emotion Rate Image')

        window.close()

if __name__ == "__main__":
    draw_page()