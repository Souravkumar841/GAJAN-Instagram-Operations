import argparse,json
from . import core as c
def main():
 p=argparse.ArgumentParser(description='GAJAN Instagram operations (human-in-loop)')
 s=p.add_subparsers(dest='cmd',required=True)
 s.add_parser('init');r=s.add_parser('register');r.add_argument('--brand',required=True);r.add_argument('--owner',required=True);r.add_argument('--handle')
 t=s.add_parser('task');t.add_argument('--account',type=int,required=True);t.add_argument('--kind',required=True);t.add_argument('--owner',required=True);t.add_argument('--days',type=int,default=1)
 d=s.add_parser('complete');d.add_argument('--task',type=int,required=True);d.add_argument('--notes',default='Human-confirmed')
 u=s.add_parser('update');u.add_argument('--account',type=int,required=True);u.add_argument('--field',required=True);u.add_argument('--value',required=True)
 s.add_parser('remind');s.add_parser('audit');o=s.add_parser('offboard');o.add_argument('--account',type=int,required=True);o.add_argument('--person',required=True)
 h=s.add_parser('health');h.add_argument('--url',default='https://example.com');g=s.add_parser('report');g.add_argument('--folder',default='artifacts')
 a=p.parse_args();c.init()
 if a.cmd=='init':v={'initialized':True}
 elif a.cmd=='register':v=c.register(a.brand,a.owner,a.handle)
 elif a.cmd=='task':v=c.task(a.account,a.kind,a.owner,a.days)
 elif a.cmd=='complete':c.complete(a.task,a.notes);v={'completed':a.task}
 elif a.cmd=='update':c.update(a.account,**{a.field:a.value});v={'updated':a.field}
 elif a.cmd=='remind':v=c.reminders()
 elif a.cmd=='audit':v=c.audit()
 elif a.cmd=='offboard':v=c.offboard(a.account,a.person)
 elif a.cmd=='health':v=c.proxy_check(a.url)
 elif a.cmd=='report':v={'folder':c.report(a.folder)}
 print(json.dumps(v,indent=2))
if __name__=='__main__':main()
