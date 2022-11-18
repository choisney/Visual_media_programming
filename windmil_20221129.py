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

def drawPolygon(cvs,pts,color):
    
    for k in range(pts.shape[0]-1):
        drawline(cvs,pts[k,0],pts[k+1,0],pts[k,1],pts[k+1,1],color)

    drawlinePQ(cvs,pts[-1],pts[0],color)

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

def getwindmill(a,b):
    wind=[]
    wind.append((0,0))
    wind.append((0,a))
    wind.append((int(a/2),b))

    return wind

def translate(ngon,points):
    P=np.ones((3,ngon))
    for i in range(ngon):
        P[0][i]=points[i][0]
        P[1][i]=points[i][1]

    return P
def getRec(a,b):
    points=[]
    points.append((a,b))
    points.append((0,b))
    points.append((0,0))
    points.append((a,0))
    points=np.array(points)
    return points



def main():
    width,height=600,600
    canvas=np.zeros((height,width,3),dtype='uint8')
    color=(225,123,255)
    color_r=(200,120,42)
    ngon = 3
    a=40
    b=20
    #기둥
    rec_pts=getRec(80,30)
    rec_pts=translate(4,rec_pts)
    rec_pts=rec_pts.astype('int')

    #풍차의 날개
    windmil=getwindmill(a,b)
    windmil=translate(ngon,windmil)

    #@할 배열들
    ct=makeTmat(width/2,height/2)
    Rotate=makeRmat(-72)
    r_ro=makeRmat(-90)
    theata=0
    #기둥의 위치
    T_1=makeTmat(0,-b/2-5)
    T_2=makeTmat(-2*a,0)
    H_1=ct@r_ro@T_1@T_2
    Q_1=(H_1@rec_pts).T
    Q_1=Q_1.astype('int')

    while True:
        canvas[:,:,:]=[0,0,0]
            #풍차의 위치
        W_1=ct
        W_2=ct@Rotate
        W_3=ct@Rotate@Rotate
        W_4=ct@Rotate@Rotate@Rotate
        W_5=ct@Rotate@Rotate@Rotate@Rotate

        R_1=makeRmat(theata)
        W_1=(W_1@R_1@windmil).T
        W_2=(W_2@R_1@windmil).T
        W_3=(W_3@R_1@windmil).T
        W_4=(W_4@R_1@windmil).T
        W_5=(W_5@R_1@windmil).T


        W_1=W_1.astype('int')
        W_2=W_2.astype('int')
        W_3=W_3.astype('int')
        W_4=W_4.astype('int')
        W_5=W_5.astype('int')


        # drawPolygon(canvas,W_1,color)
        # drawPolygon(canvas,W_2,color)
        # drawPolygon(canvas,W_3,color)
        # drawPolygon(canvas,W_4,color)
        drawPolygon(canvas,Q_1,color_r)
        fillpolygon(canvas,W_1,color)
        fillpolygon(canvas,W_2,color)
        fillpolygon(canvas,W_3,color)
        fillpolygon(canvas,W_4,color)
        fillpolygon(canvas,W_5,color)
        theata=(theata+10)%360
        cv2.imshow("window",canvas)
        if cv2.waitKey(20)==27: break

if __name__=='__main__':
    main()