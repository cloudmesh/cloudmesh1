from flask import Flask, render_template
app = Flask(__name__)




@app.route('/')
def home():

  servers = {
    u'89da179b-9540-4879-a733-c123f446f741': {
      'status': u'ACTIVE', 
      'ip': u'vlan102=10.1.2.16, 149.165.158.132', 
      'id': u'89da179b-9540-4879-a733-c123f446f741', 
      'cloud': 'india', 
      'name': u'gvonlasz-000'}, 
    u'3cdebbe0-98b0-4eb1-9f6f-6bf3725a31b4': {
      'status': u'ACTIVE', 
      'ip': u'vlan102=10.1.2.17, 149.165.158.133', 
      'id': u'3cdebbe0-98b0-4eb1-9f6f-6bf3725a31b4', 
      'cloud': 'india', 
      'name': u'gvonlasz-001'}
    }

  return render_template('home.html', servers = servers)

if __name__ == '__main__':
  app.run(debug=True)
