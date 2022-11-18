#sun, venus, earth, moon, and a rocket wondering around.

import numpy as np
import cv2

def getline(x0,y0,x1,y1):
    points=[]
    
    if (x1-x0==0):
        if y0>y1:
            for y in range(y0,y1-1,-1):
                points.append((x1,y))
        else:
            for y in range(y0,y1+1):
                points.append((x1,y))
    else:
        slope =np.abs((y1-y0)/(x1-x0))
        if slope > 1:
            if y0 > y1:
                for y in range(y0,y1-1,-1):
                    x =(y-y0)*(x1-x0)/(y1-y0)+x0 
                    points.append((x,y))

            else:
                for y in range(y0,y1+1):
                    x =(y-y0)*(x1-x0)/(y1-y0)+x0 
                    points.append((x,y))
        else:
            if x0 > x1:
                for x in range(x0,x1-1,-1):
                    y =(x-x0)*(y1-y0)/(x1-x0)+y0 
                    points.append((x,y))

            else:
                for x in range(x0,x1+1):
                    y =(x-x0)*(y1-y0)/(x1-x0)+y0
                    points.append((x,y))
    
    points=np.array(points)
    points=points.astype('int')
    return points

def drawline(canvas,x0,x1,y0,y1,color=(255,255,255)): 
    xys = getline(x0,y0,x1,y1)
    for xy in xys:
        x,y=xy
        canvas[y,x,:]=color

def deg2rad(deg):
    rad=deg*np.pi/180
    return rad

def drawlinePQ(canvas,p,q,color):
    drawline(canvas,p[0],q[0],p[1],q[1],color)
    return

def drawPolygon(cvs,pts,color, axis=False):
    
    for k in range(pts.shape[0]-1):
        drawline(cvs,pts[k,0],pts[k+1,0],pts[k,1],pts[k+1,1],color)

    drawlinePQ(cvs,pts[-1],pts[0],color)

    if axis == True: 
        center = np.array([0,0])
        for p in pts:
            center +=p
        center = center / pts.shape[0]
        center = center.astype('int')
        drawlinePQ(cvs,center,pts[0],color=(255,128,128))

def getRegularNGon(ngon):
    delta = 360/ngon
    points=[]
    for i in range (ngon):
        degree = i*delta
        radian = deg2rad(degree)
        x=np.cos(radian)
        y=np.sin(radian)
        points.append((x,y))
    points=np.array(points)
    return points


def makeTmat(a,b):
    T=np.eye(3)
    T[0,2]=a
    T[1,2]=b
    return T

def makeRmat(deg):
    rad = deg2rad(deg)
    c=np.cos(rad)
    s=np.sin(rad)
    R=np.eye(3)
    R[0,0]=c
    R[0,1]=-s
    R[1,0]=s
    R[1,1]=c
    return R

def translate(ngon,points):
    P=np.ones((3,ngon))
    for i in range(ngon):
        P[0][i]=points[i][0]
        P[1][i]=points[i][1]

    return P

def main():
    width,height=800,800
    canvas=np.zeros((height,width,3),dtype='uint8')
    color=(0,0,255)
    ngon = 5

    l=150
    a=7
    b=6
    gamma=5
    veta=5
    h=80

    #sun
    s_pts=getRegularNGon(20)
    s_pts*=50
    s_pts=translate(20,s_pts)

    T_ct=makeTmat(width/2,height/2)
    R_s_ct=makeRmat(-19)
    Q_s=T_ct@R_s_ct
    Q_s=(Q_s@s_pts).T
    Q_s=Q_s.astype('int')

    while True:
        canvas[:,:,:]=[0,0,0]
        
        #sun 그리기
        drawPolygon(canvas,Q_s,color)

        #venus speed: 35km/s 
        vn_pts=getRegularNGon(20)
        vn_pts*=20
        vn_pts=translate(20,vn_pts)

        T_vn_1=makeTmat(l,0)
        R_vn_1=makeRmat(a)
        R_vn_2=makeRmat(-a) #공전
        #R_vn_3=makeRmat(b)  #자전

        H_vn=T_ct@R_vn_1@T_vn_1@R_vn_2 #@R_vn_3
        Q_vn=(H_vn@vn_pts).T
        Q_vn=Q_vn.astype('int')
        drawPolygon(canvas,Q_vn,[50,160,130])


        #earth
        er_pts=getRegularNGon(20)
        er_pts*=30
        er_pts=translate(20,er_pts)

        T_er_1=makeTmat(250,0)
        R_er_1=makeRmat(b)
        R_er_2=makeRmat(-b)

        H_er=T_ct@R_er_1@T_er_1@R_er_2
        Q_er=(H_er@er_pts).T
        Q_er=Q_er.astype('int')
        drawPolygon(canvas,Q_er,[255,0,0])

        #moon
        m_pts=getRegularNGon(20)
        m_pts*=10
        m_pts=translate(20,m_pts)

        R_m_1=makeRmat(gamma)
        T_m_1=makeTmat(h,0)
        R_m_2=makeRmat(-gamma)

        H_mp=T_ct@R_er_1@T_er_1@R_er_2@R_m_1@T_m_1@R_m_2
        Q_mp=(H_mp@m_pts).T
        Q_mp=Q_mp.astype('int')
        drawPolygon(canvas,Q_mp,[225,220,225])

        #rocket
        r_pts=getRegularNGon(4)
        R_r=makeRmat(-45)
        r_pts=translate(4,r_pts)
        r_pts=R_r@r_pts
        r_pts[0,:]*=20
        r_pts[1,:]*=40

        T_r_1=makeTmat(350,0)
        R_r_1=makeRmat(veta)

        H_r=T_ct@R_r_1@T_r_1
        Q_r=(H_r@r_pts).T
        Q_r=Q_r.astype('int')
        drawPolygon(canvas,Q_r,[100,50,200])


        a+=6 #별,행성 (오각형 중심) 공전 속도
        b+=4 #별 자전 속도
        gamma+=2 #행성 (별 중심) 공전 속도
        veta+=5
        cv2.imshow("window",canvas)

        if cv2.waitKey(20)==27: break

if __name__=='__main__':
    main()