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

def getRec(a,b):
    points=[]
    points.append((a,b))
    points.append((0,b))
    points.append((0,0))
    points.append((a,0))
    points=np.array(points)
    return points


def translate(ngon,points):
    P=np.ones((3,ngon))
    for i in range(ngon):
        P[0][i]=points[i][0]
        P[1][i]=points[i][1]

    return P

def main():
    width,height=600,600
    canvas=np.zeros((height,width,3),dtype='uint8')
    color=(225,123,255)
    ngon = 4
    a=70;b=30
    rec_pts=getRec(a,b)
    rec_pts=translate(ngon,rec_pts)
    rec_pts=rec_pts.astype('int')
    theata=30
    gamma=20
    beta=40

    #first Rectangle (fixed)
    T_rec_ct=makeTmat(width/2,height/2)
    T_1=makeTmat(0,-b/2)
    R_1=makeRmat(-90)
    H_1=T_rec_ct@R_1@T_1
    Q_1=(H_1@rec_pts).T
    Q_1=Q_1.astype('int')
    print(Q_1)



    while True:
        canvas[:,:,:]=[0,0,0]
        drawPolygon(canvas,Q_1,color)
        T_2_1=makeTmat(a,0)
        T_2_2=makeTmat(0,b/2)
        
        #second arm(rotate)
        H_2=H_1@T_2_1@T_2_2
        R_2=makeRmat(theata)
        Q_2=(H_2@R_2@rec_pts).T
        #Q_2=(H_2@rec_pts).T :위치 확인용
        Q_2=Q_2.astype('int')
        drawPolygon(canvas,Q_2,color)
        
        #third arm(rotate)
        R_3=makeRmat(gamma)
        r_3=makeRmat(-theata)
        H_3=H_2@R_2@T_2_1@T_2_2@r_3
        Q_3=(H_3@R_3@rec_pts).T
        #Q_3=(H_3@rec_pts).T :위치 확인용
        Q_3=Q_3.astype('int')
        drawPolygon(canvas,Q_3,color)

        #forth arm(rotate)
        R_4=makeRmat(beta)
        r_4=makeRmat(-gamma)
        H_4=H_3@R_3@T_2_1@T_2_2@r_4
        Q_4=(H_4@R_4@rec_pts).T
        #Q_4=(H_4@rec_pts).T :위치 확인용
        Q_4=Q_4.astype('int')
        drawPolygon(canvas,Q_4,color)

        theata=(theata+5)%360
        gamma=(gamma+7)%360
        beta=(beta+6)%360
        cv2.imshow("window",canvas)
        if cv2.waitKey(20)==27: break

if __name__=='__main__':
    main()