import numpy as np
import matplotlib.pyplot as plt

class Path:
    def __init__(self):
        self.x=[]
        self.y=[]
        def path_add(self,other_path,x,y):
        self.x=list(other_path.x)
        self.y=list(other_path.y)

        self.x.append(x)
        self.y.append(y)
        
    
    def plot(self,ax=None):
        if ax==None:
            fig, ax = plt.subplots(figsize=(12,12))
        ax.set_aspect('equal', adjustable='box')
        ax.plot(np.array(self.x)+0.5,np.array(self.y)+0.5,color='r')
        plt.show()

class Maze(object):
    ''' Class that defines a maze'''
    def __init__(self,N=None,M=None,v_odds=0.5,h_odds=0.32,file=None,start=None):


        if file is None:
            # The cells and the walls on it
            # Dim 3: top, bottom, left, right
            cells=np.zeros((N,M,4))
            
            v_lines=np.zeros((N+1,M),dtype=bool)
            h_lines=np.zeros((N,M+1),dtype=bool)

            # Vertical
            for i in range(N+1):
                for j in range(M):
                    r_v=np.random.ranf()
                    if r_v<v_odds:
                        v_lines[i,j]=True
                    if i==0 or i==N:
                        v_lines[i,j]=True
            # Horizontal
            for i in range(N):
                for j in range(M+1):
                    
                    r_h=np.random.ranf()
                    
                    # Do the horizontal line
                    if r_h<h_odds:
                        h_lines[i,j]=True
                    if j==M:  

                        h_lines[i,j]=True

            if start is not None:
                h_lines[int(start),M]=False
            else:
                h_lines[int(N/2),M]=False

            for i in range(N):
                for j in range(M):
                    left=v_lines[i,j]
                    bottom=h_lines[i,j]
                    right=v_lines[i+1,j]
                    top=h_lines[i,j+1]
                    if top:
                        cells[i,j,0]=1
                    if bottom:
                        cells[i,j,1]=1
                    if left:
                        cells[i,j,2]=1
                    if right:
                        cells[i,j,3]=1


        
                    
            self.N=N
            self.M=M
            self.v_lines=v_lines
            self.h_lines=h_lines
            self.cells=cells
            self.path=Path()
            self.start=start
            return

        else:
            
            file_dat=np.loadtxt(file,dtype=bool).T[:,::-1]

            N,M=file_dat.shape
            v_lines=np.zeros((N+1,M),dtype=bool)
            h_lines=np.zeros((N,M+1),dtype=bool)
            cells=np.zeros((N,M,4))
            

            
            for i in range(N):
                for j in range(M):
                    if file_dat[i,j]==True:
                        v_lines[i:i+2,j]=True
                        h_lines[i,j:j+2]=True
            for i in range(N):
                for j in range(M):
                    left=v_lines[i,j]
                    bottom=h_lines[i,j]
                    right=v_lines[i+1,j]
                    top=h_lines[i,j+1]
                    if top:
                        cells[i,j,0]=1
                    if bottom:
                        cells[i,j,1]=1
                    if left:
                        cells[i,j,2]=1
                    if right:
                        cells[i,j,3]=1


 
 
            self.N=N
            self.M=M
            self.v_lines=v_lines
            self.h_lines=h_lines
            self.cells=cells
            self.path=Path()
            self.start=start
        
    def plot(self,ax=None,path=None):
        if ax==None:
            fig, ax = plt.subplots(figsize=(12,12))
        ax.set_aspect('equal', adjustable='box')
        self.ax=ax
        x=[]
        y=[]
        for i in range(self.N+1):
            for j in range(self.M):
                if self.v_lines[i,j]:
                    ax.plot([i,i],[j,j+1],color='k')
                    x.append([i,j])
                    y.append([i,j+1])
        for i in range(self.N):
            for j in range(self.M+1):
                if self.h_lines[i,j]:
                    ax.plot([i,i+1],[j,j],color='k')
                    x.append([i,j])
                    y.append([i+1,j])

        walls=ax.get_lines()
        self.walls=walls
        if path!=None:
            path.plot(ax)
        

        ax.axis('off')

        
    def cell(self,n,m):
        print(self.cells[n,m,:])

    def solve(self,plot=False):
        
        steps=np.zeros((self.N,self.M))

        if self.start is not None:
            steps[int(self.start),self.M-1]=1
        else:
            steps[int(self.N/2),self.M-1]=1
            
        done=False
        self.path=Path()
        path=np.empty(steps.shape,dtype=object)
        for i in range(self.N):
            for j in range(self.M):
                path[i,j]=Path()
        path[int(self.N/2),self.M-1].path_add(path[int(self.N/2),self.M-1],int(self.N/2),self.M-1)
                
        
        for i in range(1,50000):
            # check for the frontiers
            fronts=np.where(steps==i)
            fronts_x=fronts[0]
            fronts_y=fronts[1]
            move=False


            
            for f in range(len(fronts_x)):
                #print("No. Fronts:",len(fronts_y))

                #bottom
                if self.cells[fronts_x[f],fronts_y[f],1]==0: #No wall
                    if fronts_y[f]==0:
                        print("Path found in %d steps"%i)
                        final_path=path[fronts_x[f],fronts_y[f]]
                        done=True
               
                        break
                    if steps[fronts_x[f],fronts_y[f]-1] ==0: #Not already been here
                        steps[fronts_x[f],fronts_y[f]-1] = i+1
                        # Add to path
                        path[fronts_x[f],fronts_y[f]-1].path_add(path[fronts_x[f],fronts_y[f]],fronts_x[f],fronts_y[f]-1)
                        move=True

                #top
                if i!=1:
                    if self.cells[fronts_x[f],fronts_y[f],0]==0: #No wall
                        if fronts_y[f]!=self.M-1:
                            if steps[fronts_x[f],fronts_y[f]+1] ==0: #Not already been here
                                steps[fronts_x[f],fronts_y[f]+1] = i+1
                                # Add to path
                                path[fronts_x[f],fronts_y[f]+1].path_add(path[fronts_x[f],fronts_y[f]],fronts_x[f],fronts_y[f]+1)
                                
                                move=True
                        
                #left
                if self.cells[fronts_x[f],fronts_y[f],2]==0: #No wall
                    if fronts_x[f]!=0:
                        if steps[fronts_x[f]-1,fronts_y[f]] ==0: #Not already been here
                            steps[fronts_x[f]-1,fronts_y[f]] = i+1
                            # Add to path
                            path[fronts_x[f]-1,fronts_y[f]].path_add(path[fronts_x[f],fronts_y[f]],fronts_x[f]-1,fronts_y[f])

                            move=True
                #right
                if self.cells[fronts_x[f],fronts_y[f],3]==0: #No wall
                    if fronts_x[f]!=self.N:
                        if steps[fronts_x[f]+1,fronts_y[f]] ==0: #Not already been here
                            steps[fronts_x[f]+1,fronts_y[f]] = i+1            
                            # Add to path
                            path[fronts_x[f]+1,fronts_y[f]].path_add(path[fronts_x[f],fronts_y[f]],fronts_x[f]+1,fronts_y[f])
                        
                            move=True
            self.solved=done
            if done:

                break

            if not move:
                print("Unsolvable!")
                return

            self.steps=steps
        


            
            
        if plot:
            fig, ax = plt.subplots(figsize=(8,8))
            #ax.imshow(steps.T,extent=(0,self.N,0,self.M),origin='lower',cmap='Greys')
            self.plot(ax)
            if done:
                final_path.plot(ax)    
        self.path=final_path
    def path_to_steps(self,grid):
        
        for j in range(len(self.path.x)):            
            grid[self.path.x[j],self.path.y[j]]=10
       
        return grid

    def movie(self,filename='maze_movie.mp4'):
        from matplotlib import animation
        if not self.solved:
            return
        local_steps=self.steps
        
        fig, ax = plt.subplots(figsize=(12,12))
        self.plot(ax)
        ax.axis('off')
        im=ax.imshow(self.steps.T,extent=(0,self.N,0,self.M),origin='lower',cmap='Purples')

        def init():
            #im.set_data(np.where(self.steps-max_steps<0,0,self.steps-max_steps))
            return [im]
        
        # animation function.  This is called sequentially
        def animate(i):
            #print("Max steps:",max_steps)

            if i==0:
                a=np.zeros((self.N,self.M))
                a[int(self.N/2),self.M-1]=20.0
            elif i==int(np.max(self.steps))+1:
                a=np.where(self.steps>i-1,0,local_steps)
                a=np.where(a<i-5,0,a)-(i-5)
                a=np.where(a<0,0,a)
                a=a*20
                a=self.path_to_steps(a)
            else:
                a=np.where(self.steps>i,0,local_steps)
                a=np.where(a<i-4,0,a)-(i-4)
                a=np.where(a<0,0,a)
                a=a*20


            im.set_array(a.T)
            return [im]
        anim = animation.FuncAnimation(fig, animate, init_func=init,
                           frames=int(np.max(self.steps))+2, interval=20, blit=True)

        
        anim.save(filename, fps=10)

