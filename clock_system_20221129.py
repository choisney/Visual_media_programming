import numpy as np
import cv2
import time


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

def drawPolygon(cvs,pts,color):
    
    for k in range(pts.shape[0]-1):
        drawline(cvs,pts[k,0],pts[k+1,0],pts[k,1],pts[k+1,1],color)

    drawlinePQ(cvs,pts[-1],pts[0],color)

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

def fillpolygon(cvs,pts,color):
    line_pts=[]
    for k in range(pts.shape[0]-1):
        pt=(getline(pts[k,0],pts[k,1],pts[k+1,0],pts[k+1,1]))
        pt=pt.tolist()
        line_pts.extend(pt)
    line_pts=np.array(line_pts)
    line_pts=line_pts.astype('int')
    for j in range(len(line_pts)):
        for i in range(len(line_pts)):
            if(i==len(line_pts)-1):
                break
            drawline(cvs,line_pts[j,0],line_pts[i+1,0],line_pts[j,1],line_pts[i+1,1],color)

def translate(ngon,points):
    P=np.ones((3,ngon))
    for i in range(ngon):
        P[0][i]=points[i][0]
        P[1][i]=points[i][1]

    return P

def main():
    width,height=600,600
    canvas=np.zeros((height,width,3),dtype='uint8')
    ngon = 4
    clock=getRegularNGon(ngon)
    h_a=5;h_b=50
    m_a=5;m_b=100
    clock=translate(ngon,clock)
    clock=makeRmat(-45)@clock

    #minute size
    clock_m=np.copy(clock)
    clock_m[0,:]*=m_a
    clock_m[1,:]*=m_b
    clock_m=makeRmat(-90)@clock_m
    clock_m=clock_m.astype('int')

    #hour size
    clock[0,:]*=h_a
    clock[1,:]*=h_b
    clock=makeRmat(-90)@clock
    clock=clock.astype('int')

    #degree
    h_d=0
    m_d=0
    #move to center
    ct=makeTmat(width/2,height/2)
    R_1=makeRmat(-90)
    H_1=ct@R_1

    upper_h=makeTmat(h_b//2,0)
    upper_m=makeTmat(m_b//2,0)

    while True:
        now = time.localtime()
        m_d=now.tm_min*6
        h_d=now.tm_hour*30+now.tm_min*0.5
        canvas[:,:,:]=[0,0,0]
        H=H_1@makeRmat(h_d)@upper_h@clock
        H=H.T
        H=H.astype('int')
        drawPolygon(canvas,H,[0,255,0])
        M=H_1@makeRmat(m_d)@upper_m@clock_m
        M=M.T
        M=M.astype('int')
        drawPolygon(canvas,M,[0,0,255])


        cv2.imshow("Clock",canvas)
        if cv2.waitKey(20)==27: break

if __name__=='__main__':
    main()