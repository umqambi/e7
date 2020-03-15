from flask import render_template, request, redirect, url_for, jsonify
from flask.views import MethodView
from flask_mongoengine.wtf import model_form
from bulletin.models import Advert, Comment

class ListView(MethodView):

    def get(self):
        adverts = Advert.objects.all()
        return render_template('adverts/list.html', adverts=adverts)


class DetailView(MethodView):

    form = model_form(Comment, exclude=['created_at'])

    def get_context(self, slug):
        advert = Advert.objects.get_or_404(slug=slug)
        form = self.form(request.form)
        context = {
            "advert": advert,
            "form": form
        }
        return context

    def get(self, slug):
        context = self.get_context(slug)
        return render_template('adverts/detail.html', **context)

    def post(self, slug):
        context = self.get_context(slug)
        form = context.get('form')

        if form.validate():
            comment = Comment()
            form.populate_obj(comment)

            advert = context.get('advert')
            advert.comments.append(comment)
            advert.save()

            return redirect(url_for('adverts.detail', slug=slug))

        return render_template('adverts/detail.html', **context)

# Views for API

def api_adverts_get():
    all_ads = Advert.objects.all()
    return jsonify(all_ads)

def api_adverts_post():
    response_object = {'status': 'Success'}
    post_data = request.get_json()
    print('!!!!!!!!&&&&&&&&&&&', post_data)
    if post_data:
        if 'title' in dict.keys(post_data) and 'slug' in dict.keys(post_data) and 'body' in dict.keys(post_data):
            if not Advert.objects.filter(slug=post_data.get('slug')):
                if 'tags' in dict.keys(post_data):
                    tags = []
                    for tag in post_data.get('tags').split(','):
                        tags.append(tag.strip())
                    advert = Advert(
                        title=post_data.get('title'),
                        slug=post_data.get('slug'),
                        body=post_data.get('body'),
                        tags=tags
                    )
                else:
                    advert = Advert(
                        title=post_data.get('title'),
                        slug=post_data.get('slug'),
                        body=post_data.get('body')
                    )

                advert.save()
                response_object['message'] = 'Advert added'
                response_object['added_ad'] = advert
            else:
                response_object['status'] = 'Error'
                response_object['message'] = 'Значение поля "slug" должно быть уникально, {} уже используется'.format(post_data.get('slug'))
        else:
            response_object['status'] = 'Error'
            response_object['message'] = 'not enough data, be sure to pass: "title", "slug" and "body"'
    else:
        response_object['status'] = 'Error'
        response_object['message'] = 'No data'
    return jsonify(response_object)

def api_ad_detail_get(slug):
    if Advert.objects(slug=slug):
        return jsonify(Advert.objects(slug=slug))
    else:
        response_object = {'status': 'Error'}
        response_object['message'] = 'Advert not found'
    return jsonify(response_object)
    

def api_comment_add(slug):
    response_object = {'status': 'Success'}
    ad = Advert.objects.get(slug=slug)
    if ad:
        data = request.get_json()
        if data:
            if 'author' in dict.keys(data) and 'body' in dict.keys(data): 
                comment = Comment(
                    author = data.get('author'),
                    body = data.get('body'),
                )
                print('Допиши добавление коммента', comment)
                ad.comments.append(comment)
                ad.save()
                response_object['message'] = 'Comment added successfully'
            else:
                response_object = {'status': 'Error'}
                response_object['message'] = 'not enough data, be sure to pass: "author", and "body"'
        else:
            response_object = {'status': 'Error'}
            response_object['message'] = 'No data'
    else:
        response_object = {'status': 'Error'}
        response_object['message'] = 'Advert with slug: "{}" are not exist'.format(slug)

    return jsonify(response_object)

def api_tag_add(slug):
    response_object = {'status': 'Success'}
    ad = Advert.objects.get(slug=slug)
    if ad:
        data = request.get_json()
        if data:
            if 'tags' in dict.keys(data): 
                print(ad.tags)
                print(data.get('tags'))
                for tag in data.get('tags').split(','):
                    if not tag.strip() in ad.tags:
                        ad.tags.append(tag.strip())
                    print(ad.tags)
                    ad.save()
                response_object['message'] = 'Tags added successfully'
            else:
                response_object = {'status': 'Error'}
                response_object['message'] = 'not enough data, be sure to pass: "tags"'
        else:
            response_object = {'status': 'Error'}
            response_object['message'] = 'No data'
    else:
        response_object = {'status': 'Error'}
        response_object['message'] = 'Advert with slug: "{}" are not exist'.format(slug)

    return jsonify(response_object)

def api_ad_stat(slug):
    if Advert.objects(slug=slug):
        response_object = {'status': 'Error'}
        ad = Advert.objects.get(slug=slug)
        tcount = len(ad.tags)
        ccount = len(ad.comments)
        response_object['number of tags'] = tcount
        response_object['number of comments'] = ccount
    else:
        response_object = {'status': 'Error'}
        response_object['message'] = 'Advert not found'
    return jsonify(response_object)