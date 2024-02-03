from flask import render_template, request, redirect, abort

from app.spendings import sp_bp as bp
from app.db import get_spending_db, get_category_db


@bp.route('/')
def main_page_spendings():
    spendings = get_spending_db().get_spendings()
    spendings_dict = []
    for spending in spendings:
        spendings_dict.append({
            "id": spending[0],
            "name": spending[1],
            "category_id": spending[2],
            # "category_id": get_category_db().get_category(spending[2][0]),
            "spend_date": spending[3],
            "spending": spending[4],
            "is_spending": spending[5]
        })
    return render_template('spendings/index.html', spendings_dict=spendings_dict, categories=get_category_db())


@bp.route('/create', methods=['GET', 'POST'])
def create_spending():
    categories = get_category_db().get_categories()
    cats_names_dict = {}
    for category in categories:
        cats_names_dict[category[0]] = category[1]
    if request.method == 'GET':
        # print(get_spending_db().get_spending(16))
        # print(cats_names_dict)
        return render_template('spendings/create.html', categories_names=cats_names_dict)
    else:
        name = request.form.get('name')
        # category_id = get_category_db().get_category(request.form.get('category_id'))[0]
        category_id = request.form.get('category_id')
        spend_date = request.form.get('spend_date')
        spending = request.form.get('spending')
        is_spending = request.form.get('is_spending')

        get_spending_db().create_spending(name=name, category_id=category_id, spend_date=spend_date, spending=spending, is_spending=is_spending)
        return redirect('/spendings', code=302)


@bp.route('/edit/<int:spending_id>', methods=['GET', 'POST'])
def edit_spending(spending_id):
    categories = get_category_db().get_categories()
    cats_names_dict = {}
    for category in categories:
        cats_names_dict[category[0]] = category[1]
    if request.method == 'GET':
        spending = get_spending_db().get_spending(id=spending_id)
        if spending:
            return render_template('spendings/edit.html', name=spending[0], category_id=spending[1], spend_date=spending[2], spending=spending[3], is_spending=spending[4], categories_names=cats_names_dict, categories=get_category_db())
        abort(404)
    else:
        name = request.form.get('name')
        category_id = get_category_db().get_category(request.form.get('category_id'))[0]
        spend_date = request.form.get('spend_date')
        spending = request.form.get('spendings')
        is_spending = request.form.get('is_spending')

        get_spending_db().edit_spending(id=spending_id, name=name, category_id=category_id, spend_date=spend_date, spending=spending, is_spending=is_spending)
        return redirect('/spendings', code=302)


@bp.route('/delete/<int:spending_id>', methods=['GET', 'POST'])
def delete_spending(spending_id):
    if request.method == 'GET':
        spending = get_spending_db().get_spending(id=spending_id)
        if spending:
            return render_template('spendings/delete.html', name=spending[0])
        abort(404)
    else:
        get_spending_db().delete_spending(id=spending_id)
        return redirect('/', code=302)

@bp.route('/report')
def report():
    # print(get_spending_db().get_spending(3))
    spendings_dict = []
    for spending in get_spending_db().get_spendings():
        spendings_dict.append({
            "id": spending[0],
            "name": spending[1],
            "category_id": spending[2],
            "spend_date": spending[3],
            "spending": spending[4],
            "is_spending": spending[5]
        })

    return render_template('spendings/report.html', spendings_dict=spendings_dict, categories=get_category_db())
