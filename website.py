from flask import Flask,render_template,request
import pickle
import numpy as np
import pandas as pd


book_dict = pickle.load(open('book_dict.pkl1', 'rb'))
book = pd.DataFrame(book_dict)
similarity_scores = pickle.load(open('similarity.pkl1', 'rb'))


app = Flask(__name__)






@app.route('/recommend_books', methods=['POST'])
def recommend():
    user_input = request.form.get('user_input')
    index = np.where(book.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[:5]

    data = []
    for i in similar_items:
        item = []
        temp_df = book[book['Book Name'] == book.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book Name')['Book Name'].values))
        data.append(item)

    return render_template('recommend.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)