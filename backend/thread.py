from threading import Thread, Event
from app import app

app_port = 8000
announce_url = None
cloudflared_startup = Event()

def update_announce_url(url):
    global announce_url
    announce_url = url

def start_cloudflared(port):
  from flask_cloudflared import _run_cloudflared
  try:
    announce_url = _run_cloudflared(port, 8888)
  except:
    raise
  finally:
    update_announce_url(announce_url)
    cloudflared_startup.set()

def run_with_cloudflared(thread):
    old_run = thread.run

    def new_run(*args, **kwargs):
        new_thread = Thread(target = start_cloudflared, args=(app_port, ))
        new_thread.setDaemon(True)
        new_thread.start()
        old_run(*args, **kwargs)

    thread.run = new_run

def run_app():
    app.run(host="0.0.0.0", port=8000, debug=False)

if __name__ == '__main__':
    t1 = Thread(target = run_app)
    run_with_cloudflared(t1)
    t1.start()
    cloudflared_startup.wait()
    print(f"Your url is: {announce_url}")
    t1.join()