import cv2
import numpy as np

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

def translate(ngon,points):
    P=np.ones((3,ngon))
    for i in range(ngon):
        P[0][i]=points[i][0]
        P[1][i]=points[i][1]

    return P

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

def getStar(canvas,pts,ngon,color):
    for i in range(ngon-2):
        for j in range(2):
            if(i+j>=3):break
            drawline(canvas,pts[0,i],pts[0,i+j+2],pts[1,i],pts[1,i+j+2],color)


def main():
    w,h=500,500
    canvas=np.zeros((h,w,3),dtype='uint8')
    st=getRegularNGon(5)
    st*=100
    st=translate(5,st)

    while True:

        while True:
            check=1
            position=makeTmat(np.random.randint(w),np.random.randint(h))
            rotate=makeRmat(np.random.randint(360))
            Q_star=(position@rotate@st)
            for i in range(5):
                if Q_star[0,i]>=500 or Q_star[1,i]>=500:
                    check=0
                    continue
            if check==1: break
        
        Q_star=Q_star.astype('int')
        getStar(canvas,Q_star,5,[np.random.randint(255),np.random.randint(255),np.random.randint(255)])
        cv2.imshow("twinkle",canvas)

        if cv2.waitKey(20)==27: 
                break


if __name__=='__main__':
    main()