/**摄像机管理器
 * 引擎本来没有摄像机这一概念，这里只是通过对GameMap的参数控制，实现类似摄像机的功能
 * 摄像机只有一个
 */
class Camera extends BaseClass {

	/**关注目标 */
	public static target: Entity;
	private static _map: GameMap = null;
	/**地图实体 摄像机运动都是通过改变这个对象的参数实现 */
	public static get map(): GameMap {
		if (this._map == null) {
			this._map = GameMap.ins();
			this.zoomTo(1);
		}
		return this._map;
	};

	public static OFFSET_Y: number = 115;

	/**摄像机坐标 X*/
	public static get x(): number {
		let rtn = 0;
		if (this.map) {
			rtn = -this.map.x;
		}
		return rtn;
	}

	/**摄像机坐标 X*/
	public static set x(value: number) {
		if (this.map) {
			this.map.x = -value;
		}
	}

	/**摄像机坐标 Y*/
	public static get y(): number {
		let rtn = 0;
		if (this.map) {
			rtn = -this.map.y;
		}
		return rtn;
	}

	/**摄像机坐标 Y*/
	public static set y(value: number) {
		if (this.map) {
			this.map.y = -value;
		}
	}

	/**摄像机缩放*/
	public static get scale(): number {
		let rtn = 0;

		if (this.map) {
			rtn = this.map.scaleX;
		}
		return rtn;
	}

	/**摄像机缩放*/
	public static set scale(value: number) {
		if (this.map) {
			this.map.scaleX = this.map.scaleY = value;
		}
	}

	public static myEntity(): EntityRole {
		return this.target as EntityRole;
	}

	public static clearLookAt(): null {
		return this.target = null;
	}

	public static worldToLocal(x: number, y: number): egret.Point {
		let point: egret.Point = new egret.Point();
		point.x = x - this.x;
		point.y = y - this.y;
		return point;
	}

	/**定点看某个对象 */
	public static lookAtTarget(target: any): void {
		this.target = target;
		let sw = StageUtils.ins().getWidth();
		let sh = StageUtils.ins().getHeight() - GameMap.MAINUI_NAV_HEIGHT;
		let x = (target.x - sw / 2) * this.scale + sw * (this.scale / 2 - 0.5);
		let y = (target.y - this.OFFSET_Y - sh / 2) * this.scale + sh * (this.scale / 2 - 0.5);
		this.x = Math.min(Math.max(x, 0), this.map.MAX_WIDTH * this.scale - sw);
		this.y = Math.min(Math.max(y, 0), this.map.MAX_HEIGHT * this.scale - sh);
		this.map.updateHDMap(-this.x, -this.y, false);
		this.doCameraMoving();
	}

	/**
	*   从某个坐标去某个坐标，停顿一定时间，原路返回
	*/
	public static moveToAndBack(endX: number, endY: number, goTime: number = 400, backTime: number = 500, delayTime: number = 1000) {
		let self = this;
		egret.Tween.removeTweens(self);
		let beginX: number = self.x;
		let beginY: number = self.y;
		endX = endX * this.x + StageUtils.ins().getWidth() * (this.scale / 2 - 0.5);
		endY = endY * this.y + StageUtils.ins().getHeight() * (this.scale / 2 - 0.5);
		let tw = egret.Tween.get(self, {
			onChange: function (): void {
				self.map.updateHDMap(this.x, this.y);
			}
		});
		tw.to({ CameraPosX: endX, CameraPosY: endY }, goTime, egret.Ease.sineIn)
			.wait(delayTime)
			.to({ CameraPosX: beginX, CameraPosY: beginY }, backTime, egret.Ease.sineIn);
	}

	/**移动到某一点 */
	public static moveTo(endX: number, endY: number, goTime: number = 400, waitTime: number = 400, callBaack: Function = () => { }) {
		let self = this;
		endX = endX * this.scale + StageUtils.ins().getWidth() * (this.scale / 2 - 0.5);
		endY = endY * this.scale + StageUtils.ins().getHeight() * (this.scale / 2 - 0.5);
		egret.Tween.removeTweens(self);
		let tw = egret.Tween.get(self, {
			onChange: function (): void {
				self.map.updateHDMap(this.x, this.y);
			}
		});
		tw.to({ CameraPosX: endX, CameraPosY: endY }, goTime, egret.Ease.sineIn).wait(waitTime).call(callBaack);
	}

	/**
	 * @主角玩家走路统一接口
	 * @path 移动路径
	 * @func 回调函数
	 * @obj  回调对象
	 */
	public static doWalk(path: number[], onComplete: () => void = null, obj: Entity = Camera.target, fun: string = "", type: WalkType = WalkType.None): void {
		if (BufferModel.ins().checkNoMoveBuff()) return;
		//点击地图屏蔽主界面组件
		let topView = ViewManager.ins().getView("MainUI_TopView") as MainUI_TopView;
		if (topView) topView.hidenComponent();

		let role = Camera.myEntity();
		if (role.isDead()) return;
		role.setMountEffPoint();
		if (path && path.length) {
			role.startMove(path, onComplete, obj);
			//跟随示范例子
			// TimerManager.ins().doNext(()=>{FollowerManager.ins().followerMove(path)},this);
			//TimerManager.ins().doNext(()=>{FollowerManager.ins().petFollowerMove(path)},this);
			// TimerManager.ins().doNext(()=>{FollowerManager.ins().followerMove(Camera.target,path)},this);
			if (type == WalkType.Drop) {

			}
			else {
				TimerManager.ins().doNext(() => { FollowerManager.ins().followerMove(role, path) }, this);
			}
		}

		if (!HangMgr.ins().hangUp) {
			HangMgr.ins().removeAutoTimer();
		}
		// if (Debug.isDebug) {
		// 	Debug.log("function=" + fun + " path" + path);
		// 	if (obj) {
		// 		Debug.log("function=" + fun + " name=" + obj.getName() + "pox = " + obj.x + "poY=" + obj.y);
		// 	}
		// }	
	}

	public static dirTo(dir: number): void {
		// HangMgr.ins().stopHang()
		// Camera.target.dirTo(dir);
		// FollowerManager.ins().followerMove([Camera.target.x, Camera.target.y]);
	}

	/**
	*   镜头缩放
	*/
	public static zoomTo(zoomScale: number = 1.4, zoomInTime: number = 200, waitTime: number = 0, callBaack: Function = () => { }) {
		let self = this;
		egret.Tween.removeTweens(self);
		let tw = egret.Tween.get(self, {
			onChange: function (): void {
				if (self.target)
					self.lookAtTarget(self.target)
			}
		});
		tw.to({ scale: zoomScale }, zoomInTime).wait(waitTime).call(callBaack);
	}

	public static defaultPosX: number = 0;
	public static defaultPosY: number = 0;
	public static resetCamera(): void {
		this.x = Camera.defaultPosX;
		this.y = Camera.defaultPosY;
	}

	public static doCameraMoving(): XY {
		return { x: Camera.x, y: Camera.y }
	}
}

namespace ComplieClass {
	export let cameraClass = () => {
		MessageCenter.compile(Camera);
	};
}
window["Camera"] = Camera;