from recordtype import recordtype

import numpy as np
from numpy import array
import xarray as xr
import matplotlib.pyplot as plt
import time
from collections import deque

# TODO: suggested renaming to RailEnvRenderTool, as it will only work with RailEnv!

class RenderTool(object):
    Visit = recordtype("Visit", ["rc", "iDir", "iDepth", "prev"])

    lColors = list("brgcmyk")
    # \delta RC for NESW
    gTransRC = np.array([[-1, 0], [0, 1], [1, 0], [0, -1]])
    nPixCell = 1
    nPixHalf = nPixCell / 2
    xyHalf = array([nPixHalf, -nPixHalf])
    grc2xy = array([[0, -nPixCell], [nPixCell, 0]])
    gGrid = array(np.meshgrid(np.arange(10), -np.arange(10))) * \
        array([[[nPixCell]], [[nPixCell]]])
    xyPixHalf = xr.DataArray([nPixHalf, -nPixHalf],
                             dims="xy",
                             coords={"xy": ["x", "y"]})
    gCentres = xr.DataArray(gGrid,
                            dims=["xy", "p1", "p2"],
                            coords={"xy": ["x", "y"]}) + xyPixHalf
    gTheta = np.linspace(0, np.pi/2, 10)
    gArc = array([np.cos(gTheta), np.sin(gTheta)]).T  # from [1,0] to [0,1]

    def __init__(self, env):
        self.env = env
        self.iFrame = 0
        self.time1 = time.time()
        self.lTimes = deque()

    def plotTreeOnRail(self, lVisits, color="r"):
        """
        Derives and plots a tree of transitions starting at position rcPos
        in direction iDir.
        Returns a list of Visits which are the nodes / vertices in the tree.
        """
        # gGrid = np.meshgrid(np.arange(10), -np.arange(10))
        rt = self.__class__
        # plt.scatter(*rt.gCentres, s=5, color="r")

        if False:
            for iAgent in range(self.env.number_of_agents):
                sColor = rt.lColors[iAgent]

                rcPos = self.env.agents_position[iAgent]
                iDir = self.env.agents_direction[iAgent]  # agent dir index

                self.plotAgent(rcPos, iDir, sColor)

                gTransRCAg = self.getTransRC(rcPos, iDir)
                self.plotTrans(rcPos, gTransRCAg, color=color)

                if False:
                    # TODO: this was `rcDir' but it was undefined
                    rcNext = rcPos + iDir
                    # transition for next cell
                    tbTrans = self.env.rail.get_transitions((*rcNext, iDir))
                    giTrans = np.where(tbTrans)[0]  # RC list of transitions
                    gTransRCAg = rt.gTransRC[giTrans]

        for visit in lVisits:
            # transition for next cell
            tbTrans = self.env.rail.get_transitions((*visit.rc, visit.iDir))
            giTrans = np.where(tbTrans)[0]  # RC list of transitions
            gTransRCAg = rt.gTransRC[giTrans]
            self.plotTrans(visit.rc, gTransRCAg, depth=str(visit.iDepth), color=color)

    def plotAgents(self):
        rt = self.__class__

        # plt.scatter(*rt.gCentres, s=5, color="r")

        for iAgent in range(self.env.number_of_agents):
            sColor = rt.lColors[iAgent]

            rcPos = self.env.agents_position[iAgent]
            iDir = self.env.agents_direction[iAgent]  # agent direction index

            self.plotAgent(rcPos, iDir, sColor)

            gTransRCAg = self.getTransRC(rcPos, iDir)
            self.plotTrans(rcPos, gTransRCAg)

    def getTransRC(self, rcPos, iDir, bgiTrans=False):
        """
        Get the available transitions for rcPos in direction iDir,
        as row & col deltas.

        If bgiTrans is True, return a grid of indices of available transitions.

        eg for a cell rcPos = (4,5), in direction iDir = 0 (N),
        where the available transitions are N and E, returns:
        [[-1,0], [0,1]] ie N=up one row, and E=right one col.
        and if bgiTrans is True, returns a tuple:
        (
            [[-1,0], [0,1]], # deltas as before
            [0, 1] #  available transition indices, ie N, E
        )
        """

        tbTrans = self.env.rail.get_transitions((*rcPos, iDir))
        giTrans = np.where(tbTrans)[0]  # RC list of transitions

        # HACK: workaround dead-end transitions
        if len(giTrans) == 0:
            # print("Dead End", rcPos, iDir, tbTrans, giTrans)
            iDirReverse = (iDir + 2) % 4
            tbTrans = tuple(int(iDir2 == iDirReverse) for iDir2 in range(4))
            giTrans = np.where(tbTrans)[0]  # RC list of transitions
            # print("Dead End2", rcPos, iDirReverse, tbTrans, giTrans)

        # print("agent", array(list("NESW"))[giTrans], self.gTransRC[giTrans])
        gTransRCAg = self.__class__.gTransRC[giTrans]

        if bgiTrans:
            return gTransRCAg, giTrans
        else:
            return gTransRCAg

    def plotAgent(self, rcPos, iDir, sColor="r"):
        """
        Plot a simple agent.
        Assumes a working matplotlib context.
        """
        rt = self.__class__
        xyPos = np.matmul(rcPos, rt.grc2xy) + rt.xyHalf
        plt.scatter(*xyPos, color=sColor)            # agent location

        rcDir = rt.gTransRC[iDir]                    # agent direction in RC
        xyDir = np.matmul(rcDir, rt.grc2xy)          # agent direction in xy
        xyDirLine = array([xyPos, xyPos+xyDir/2]).T  # line for agent orient.
        plt.plot(*xyDirLine, color=sColor, lw=5, ms=0, alpha=0.6)

        # just mark the next cell we're heading into
        rcNext = rcPos + rcDir
        xyNext = np.matmul(rcNext, rt.grc2xy) + rt.xyHalf
        plt.scatter(*xyNext, color=sColor)

    def plotTrans(self, rcPos, gTransRCAg, color="r", depth=None):
        """
        plot the transitions in gTransRCAg at position rcPos.
        gTransRCAg is a 2d numpy array containing a list of RC transitions,
        eg [[-1,0], [0,1]] means N, E.

        """

        rt = self.__class__
        xyPos = np.matmul(rcPos, rt.grc2xy) + rt.xyHalf
        gxyTrans = xyPos + np.matmul(gTransRCAg, rt.grc2xy/2.4)
        plt.scatter(*gxyTrans.T, color=color, marker="o", s=50, alpha=0.2)
        if depth is not None:
            for x, y in gxyTrans:
                plt.text(x, y, depth)

    def getTreeFromRail(self, rcPos, iDir, nDepth=10, bBFS=True, bPlot=False):
        """
        Generate a tree from the env starting at rcPos, iDir.
        """
        rt = self.__class__
        print(rcPos, iDir)
        iPos = 0 if bBFS else -1  # BF / DF Search

        iDepth = 0
        visited = set()
        lVisits = []
        # stack = [ (rcPos,iDir,nDepth) ]
        stack = [rt.Visit(rcPos, iDir, iDepth, None)]
        while stack:
            visit = stack.pop(iPos)
            rcd = (visit.rc, visit.iDir)
            if visit.iDepth > nDepth:
                continue
            lVisits.append(visit)

            if rcd not in visited:
                visited.add(rcd)

                # moves = self._get_valid_transitions( node[0], node[1] )
                gTransRCAg, giTrans = self.getTransRC(visit.rc,
                                                      visit.iDir,
                                                      bgiTrans=True)
                # nodePos = node[0]

                # enqueue the next nodes (ie transitions from this node)
                for gTransRC2, iTrans in zip(gTransRCAg, giTrans):
                    # print("Trans:", gTransRC2)
                    visitNext = rt.Visit(tuple(visit.rc + gTransRC2),
                                         iTrans,
                                         visit.iDepth+1,
                                         visit)
                    # print("node2: ", node2)
                    stack.append(visitNext)

                # plot the available transitions from this node
                if bPlot:
                    self.plotTrans(
                        visit.rc, gTransRCAg,
                        depth=str(visit.iDepth))

        return lVisits

    def plotTree(self, lVisits, xyTarg):
        '''
        Plot a vertical tree of transitions.
        Returns the "visit" to the destination
        (ie where euclidean distance is near zero) or None if absent.
        '''

        dPos = {}
        iPos = 0

        visitDest = None

        for iVisit, visit in enumerate(lVisits):

            if visit.rc in dPos:
                xLoc = dPos[visit.rc]
            else:
                xLoc = dPos[visit.rc] = iPos
                iPos += 1

            rDist = np.linalg.norm(array(visit.rc) - array(xyTarg))
            # sDist = "%.1f" % rDist

            xLoc = rDist + visit.iDir / 4

            # point labelled with distance
            plt.scatter(xLoc, visit.iDepth,  color="k", s=2)
            # plt.text(xLoc, visit.iDepth, sDist, color="k", rotation=45)
            plt.text(xLoc, visit.iDepth, visit.rc, color="k", rotation=45)

            # if len(dPos)>1:
            if visit.prev:
                # print(dPos)
                # print(tNodeDepth)
                xLocPrev = dPos[visit.prev.rc]

                rDistPrev = np.linalg.norm(array(visit.prev.rc) -
                                           array(xyTarg))
                # sDist = "%.1f" % rDistPrev

                xLocPrev = rDistPrev + visit.prev.iDir / 4

                # line from prev node
                plt.plot([xLocPrev, xLoc],
                         [visit.iDepth-1, visit.iDepth],
                         color="k", alpha=0.5, lw=1)

            if rDist < 0.1:
                visitDest = visit

        # Walk backwards from destination to origin, plotting in red
        if visitDest is not None:
            visit = visitDest
            xLocPrev = None
            while visit is not None:
                rDist = np.linalg.norm(array(visit.rc) - array(xyTarg))
                xLoc = rDist + visit.iDir / 4
                if xLocPrev is not None:
                    plt.plot([xLoc, xLocPrev], [visit.iDepth, visit.iDepth+1],
                             color="r", alpha=0.5, lw=2)
                xLocPrev = xLoc
                visit = visit.prev
            # prev = prev.prev

        # plt.xticks(range(7)); plt.yticks(range(11))
        ax = plt.gca()
        plt.xticks(range(int(ax.get_xlim()[1])+1))
        plt.yticks(range(int(ax.get_ylim()[1])+1))
        plt.grid()
        plt.xlabel("Euclidean distance")
        plt.ylabel("Tree / Transition Depth")
        return visitDest

    def plotPath(self, visitDest):
        """
        Given a "final" visit visitDest, plotPath recurses back through the path
        using the visit.prev field (previous) to get back to the start of the path.
        The path of transitions is plotted with arrows at 3/4 along the line.
        The transition is plotted slightly to one side of the rail, so that
        transitions in opposite directions are separate.
        Currently, no attempt is made to make the transition arrows coincide
        at corners, and they are straight only.
        """

        rt = self.__class__
        # Walk backwards from destination to origin
        if visitDest is not None:
            visit = visitDest
            xyPrev = None
            while visit is not None:
                xy = np.matmul(visit.rc, rt.grc2xy) + rt.xyHalf
                if xyPrev is not None:
                    dx, dy = (xyPrev - xy) / 20
                    xyLine = array([xy, xyPrev]) + array([dy, dx])

                    plt.plot(*xyLine.T, color="r", alpha=0.5, lw=1)

                    xyMid = np.sum(xyLine * [[1/4], [3/4]], axis=0)

                    xyArrow = array([
                        xyMid + [-dx-dy, +dx-dy],
                        xyMid,
                        xyMid + [-dx+dy, -dx-dy]
                        ])
                    plt.plot(*xyArrow.T, color="r")

                visit = visit.prev
                xyPrev = xy

    def drawTrans2(
            self,
            xyLine, xyCentre,
            rotation, bDeadEnd=False,
            sColor="gray",
            bArrow=True,
            spacing=0.1):
        """
        gLine is a numpy 2d array of points,
        in the plotting space / coords.
        eg:
        [[0,.5],[1,0.2]] means a line
        from x=0, y=0.5
        to   x=1, y=0.2
        """
        rt = self.__class__
        bStraight = rotation in [0, 2]
        dx, dy = np.squeeze(np.diff(xyLine, axis=0)) * spacing / 2

        if bStraight:

            if sColor == "auto":
                if dx > 0 or dy > 0:
                    sColor = "C1"   # N or E
                else:
                    sColor = "C2"   # S or W

            if bDeadEnd:
                xyLine2 = array([
                    xyLine[1] + [dy, dx],
                    xyCentre,
                    xyLine[1] - [dy, dx],
                ])
                plt.plot(*xyLine2.T, color=sColor)
            else:
                xyLine2 = xyLine + [-dy, dx]
                plt.plot(*xyLine2.T, color=sColor)

                if bArrow:
                    xyMid = np.sum(xyLine2 * [[1/4], [3/4]], axis=0)

                    xyArrow = array([
                        xyMid + [-dx-dy, +dx-dy],
                        xyMid,
                        xyMid + [-dx+dy, -dx-dy]
                        ])
                    plt.plot(*xyArrow.T, color=sColor)

        else:

            xyMid = np.mean(xyLine, axis=0)
            dxy = xyMid - xyCentre
            xyCorner = xyMid + dxy
            if rotation == 1:
                rArcFactor = 1 - spacing
                sColorAuto = "C1"
            else:
                rArcFactor = 1 + spacing
                sColorAuto = "C2"
            dxy2 = (xyCentre - xyCorner) * rArcFactor  # for scaling the arc

            if sColor == "auto":
                sColor = sColorAuto

            plt.plot(*(rt.gArc * dxy2 + xyCorner).T, color=sColor)

            if bArrow:
                dx, dy = np.squeeze(np.diff(xyLine, axis=0)) / 20
                iArc = int(len(rt.gArc) / 2)
                xyMid = xyCorner + rt.gArc[iArc] * dxy2
                xyArrow = array([
                    xyMid + [-dx-dy, +dx-dy],
                    xyMid,
                    xyMid + [-dx+dy, -dx-dy]
                    ])
                plt.plot(*xyArrow.T, color=sColor)

    def renderEnv(
            self, show=False, curves=True, spacing=False,
            arrows=False, agents=True, sRailColor="gray",
            frames=False, iEpisode=None, iStep=None):
        """
        Draw the environment using matplotlib.
        Draw into the figure if provided.

        Call pyplot.show() if show==True.
        (Use show=False from a Jupyter notebook with %matplotlib inline)
        """

        # cell_size is a bit pointless with matplotlib - it does not relate to pixels,
        # so for now I've changed it to 1 (from 10)
        cell_size = 1
        plt.clf()
        # if oFigure is None:
        #    oFigure = plt.figure()

        def drawTrans(oFrom, oTo, sColor="gray"):
            plt.plot(
                [oFrom[0], oTo[0]],  # x
                [oFrom[1], oTo[1]],  # y
                color=sColor
            )

        env = self.env

        # Draw cells grid
        grid_color = [0.95, 0.95, 0.95]
        for r in range(env.height+1):
            plt.plot([0, (env.width+1)*cell_size],
                     [-r*cell_size, -r*cell_size],
                     color=grid_color)
        for c in range(env.width+1):
            plt.plot([c*cell_size, c*cell_size],
                     [0, -(env.height+1)*cell_size],
                     color=grid_color)

        # Draw each cell independently
        for r in range(env.height):
            for c in range(env.width):

                # bounding box of the grid cell
                x0 = cell_size * c       # left
                x1 = cell_size * (c+1)   # right
                y0 = cell_size * -r      # top
                y1 = cell_size * -(r+1)  # bottom

                # centres of cell edges
                coords = [
                    ((x0+x1)/2.0, y0),  # N middle top
                    (x1, (y0+y1)/2.0),  # E middle right
                    ((x0+x1)/2.0, y1),  # S middle bottom
                    (x0, (y0+y1)/2.0)   # W middle left
                ]

                # cell centre
                xyCentre = array([x0, y1]) + cell_size / 2

                # cell transition values
                oCell = env.rail.get_transitions((r, c))

                # Special Case 7, with a single bit; terminate at center
                nbits = 0
                tmp = oCell

                while tmp > 0:
                    nbits += (tmp & 1)
                    tmp = tmp >> 1

                # as above - move the from coord to the centre
                # it's a dead env.
                bDeadEnd = nbits == 1

                for orientation in range(4):  # ori is where we're heading
                    from_ori = (orientation + 2) % 4  # 0123=NESW -> 2301=SWNE
                    from_xy = coords[from_ori]

                    # renderer.push()
                    # renderer.translate(c * CELL_PIXELS, r * CELL_PIXELS)

                    tMoves = env.rail.get_transitions((r, c, orientation))

                    # to_ori = (orientation + 2) % 4
                    for to_ori in range(4):
                        to_xy = coords[to_ori]
                        rotation = (to_ori - from_ori) % 4

                        if (tMoves[to_ori]):  # if we have this transition

                            if bDeadEnd:
                                self.drawTrans2(
                                    array([from_xy, to_xy]), xyCentre,
                                    rotation, bDeadEnd=True, spacing=spacing,
                                    sColor=sRailColor)

                            else:

                                if curves:
                                    self.drawTrans2(
                                        array([from_xy, to_xy]), xyCentre,
                                        rotation, spacing=spacing, bArrow=arrows,
                                        sColor=sRailColor)
                                else:
                                    drawTrans(from_xy, to_xy, sRailColor)

                            if False:
                                print(
                                    "r,c,ori: ", r, c, orientation,
                                    "cell:", "{0:b}".format(oCell),
                                    "moves:", tMoves,
                                    "from:", from_ori, from_xy,
                                    "to: ", to_ori, to_xy,
                                    "cen:", *xyCentre,
                                    "rot:", rotation,
                                )

        # Draw each agent + its orientation + its target
        if agents:
            cmap = plt.get_cmap('hsv', lut=env.number_of_agents+1)
            for i in range(env.number_of_agents):
                self._draw_square((
                                env.agents_position[i][1] *
                                cell_size+cell_size/2,
                                -env.agents_position[i][0] *
                                cell_size-cell_size/2),
                                cell_size/8, cmap(i))
            for i in range(env.number_of_agents):
                self._draw_square((
                                env.agents_target[i][1] *
                                cell_size+cell_size/2,
                                -env.agents_target[i][0] *
                                cell_size-cell_size/2),
                                cell_size/3, [c for c in cmap(i)])

                # orientation is a line connecting the center of the cell to the
                # side of the square of the agent
                new_position = env._new_position(env.agents_position[i], env.agents_direction[i])
                new_position = ((
                    new_position[0] + env.agents_position[i][0]) / 2 * cell_size,
                    (new_position[1] + env.agents_position[i][1]) / 2 * cell_size)

                plt.plot(
                    [env.agents_position[i][1] * cell_size+cell_size/2, new_position[1]+cell_size/2],
                    [-env.agents_position[i][0] * cell_size-cell_size/2, -new_position[0]-cell_size/2],
                    color=cmap(i),
                    linewidth=2.0)

        # Draw some textual information like fps
        yText = [0.1, 0.4, 0.7]
        if frames:
            plt.text(0.1, yText[2], "Frame:{:}".format(self.iFrame))
        self.iFrame += 1
        
        if iEpisode is not None:
            plt.text(0.1, yText[1], "Ep:{}".format(iEpisode))

        if iStep is not None:
            plt.text(0.1, yText[0], "Step:{}".format(iStep))

        tNow = time.time()
        plt.text(2, yText[2], "elapsed:{:.2f}s".format(tNow - self.time1))
        self.lTimes.append(tNow)
        if len(self.lTimes) > 20:
            self.lTimes.popleft()
        if len(self.lTimes) > 1:
            rFps = (len(self.lTimes) - 1) / (self.lTimes[-1] - self.lTimes[0])
            plt.text(2, yText[1], "fps:{:.2f}".format(rFps))

        plt.xlim([0, env.width * cell_size])
        plt.ylim([-env.height * cell_size, 0])

        gTicks = (np.arange(0, env.height) + 0.5) * cell_size
        gLabels = np.arange(0, env.height)
        plt.xticks(gTicks, gLabels)

        gTicks = np.arange(-env.height * cell_size, 0) + cell_size/2
        gLabels = np.arange(env.height-1, -1, -1)
        plt.yticks(gTicks, gLabels)

        plt.xlim([0, env.width * cell_size])
        plt.ylim([-env.height * cell_size, 0])
        if show:
            plt.show(block=False)
            plt.pause(0.00001)
            return

    def _draw_square(self, center, size, color):
        x0 = center[0]-size/2
        x1 = center[0]+size/2
        y0 = center[1]-size/2
        y1 = center[1]+size/2
        plt.plot([x0, x1, x1, x0, x0], [y0, y0, y1, y1, y0], color=color)
