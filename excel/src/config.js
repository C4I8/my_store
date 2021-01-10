const config = {}
config.sheetconfig = {
    "关卡种子": "scenes",
    "关卡数据种子": "timeLine_scenes",
    "领地关卡种子": "manorScenes",
    "领地关卡数据种子": "timeLine_manorScenes",
    "试炼关卡种子": "expScenes",
    "试炼关卡数据种子": "timeLine_expScenes",
    "单位种子": "units",
    "道具": "items",
    "成就": "achievements",
    "兵营晋升表": "lvBarrack",
    "段位表": "mactchLevel",
    "领地表": "manor",
    "科技表": "technology",
    "技能表": "skills",
    "雕像": "towns",
    "物品表": "goods",
    "宝箱表": "awardboxs",
    "抽卡表": "cards",
    "商店表": "shops",
    "英雄等级表": "heroLv",
    "游戏控制表": "gamecontroll",
    "危机目标": "crisistgsdic",
    "剧情表": "plotsdic",
    "英雄装备表": "equipdic",
    "星座表": "constelldic"
}

config.sheetconfigsub = {
    "scenes": {
        attr: "timeLine",
        sonsheetname: "timeLine_scenes",
        sonconfig: "timeLine_sub",
        parentindexname: "id",
        sonindexname: "sceneId"
    },
    "manorScenes": {
        attr: "timeLine",
        sonsheetname: "timeLine_manorScenes",
        sonconfig: "timeLine_sub",
        parentindexname: "id",
        sonindexname: "sceneId"
    },
    "expScenes": {
        attr: "timeLine",
        sonsheetname: "timeLine_expScenes",
        sonconfig: "timeLine_sub",
        parentindexname: "id",
        sonindexname: "sceneId"
    }
}


config.timeLine_sub = {
    "关卡ID": ["sceneId", "number"],
    "时间": ["timeAt", "number"],
    "单位": ["uid", "int_split"],
    "数量": ["num", "number"],
    "所属": ["team", "int_split"],
    "位置X": ["offX", "number"],
    "生命系数": ["hpRate", "number"],
    "攻击系数": ["atkRate", "number"],
    "基地血量": ["towerFireHpRate", "number"],
    "台词泡泡": ["popText", "number"],
    "泡泡头像": ["popFaceId", "number"],
    "赏金": ["getcoin", "number"],
    "敌对道具": ["getItemID", "number"],
    "敌对道具说明": ["getItemDesc", "string"],
    "气泡位置": ["qipaoalgen", "string"]
}

config.scenes = {
    "关卡ID": ["id", "number"],
    "名字": ["name", "string"],
    "我方矿数": ["ourMines", "number"],
    "敌方矿数": ["enemyMines", "number"],
    "中间矿数": ["centerMines", "number"],
    "战场宽度": ["sceneWidth", "number"],
    "胜利条件": ["sceneType", "int_split"],
    "我方初始金币": ["startGold", "number"],
    "敌方初始金币": ["enemyGold", "number"],
    "背景": ["sceneBG", "number"],
    "我方建造列表": ["ourUnits", "int_array"],
    "敌方建造列表": ["enemyUnits", "int_array"],
    "我方建造速度": ["ourBuildCostTime", "number"],
    "敌方建造速度": ["enemyBuildCostTime", "number"],
    "敌方战斗人口上限": ["enemyMaxPeople", "number"],
    "最低进攻人口": ["atkBP", "number"],
    "进攻策略": ["AIAttack", "int_split"],
    "撤退策略": ["AIFallback", "int_split"],
    "开场剧情介绍文字": ["startDesc", "string"],
    "通关文字": ["winString", "string"],
    "失败文字": ["failString", "string"],
    "通关解锁显示": ["unlocks", "string"],
    "通关经验": ["rewardExp", "number"],
    "我方主基": ["bldMyTown", "number"],
    "战斗限时": ["limitTime", "number"],
    "首次奖励": ["firstreward", "string"],
    "敌方星级": ["enemystar", "number"],
    "阶段任务": ["stagetask", "string"],
    "BGM": ["BGM", "string"],
    "通关第几关解锁": ["unlocklevel", "number"],
    "首次消耗后勤": ["logistics", "number"],
    "危机目标": ["crisistargets", "string"],
    "开始剧情": ["startplotid", "number"],
    "结束剧情": ["endplotid", "number"],
    "敌方总数": ["enemyallnum", "number"],
    "推荐兵种": ["tuijunits", "string"],
    "电脑出战阵型排序": ["aiunitOrder", "int_array"],
    "通关奖励物品ID和数量": ["rewardStr", "string"]
}

config.manorScenes = config.scenes;

config.expScenes = config.scenes;

config.units = {
    "ID": ["id", "number"],
    "名字": ["name", "string"],
    "职业": ["job", "int_split"],
    "单位技能ID": ["sklId", "number"],
    "生命": ["hp", "number"],
    "攻击": ["atk", "number"],
    "防御": ["def", "number"],
    "索敌范围": ["scanRange", "number"],
    "移动速度": ["spd", "number"],
    "攻击速度": ["atkSpd", "number"],
    "造价": ["cost", "number"],
    "人口": ["people", "number"],
    "建造时间": ["costTime", "number"],
    "攻击CD": ["atkCD", "number"],
    "对建筑伤害修正": ["dmgRateForStatus", "number"],
    "会离特别近再打": ["closeAtk", "number"],
    "是否受科技影响": ["equipSklLvUp", "number"],
    "皮肤名称": ["skinName", "string"],
    "单位说明": ["des", "string"],
    "招募费用": ["unlockcost", "number"],
    "物资": ["starCost", "number"],
    "攻击类型": ["typeAtk", "int_split"],
    "护甲类型": ["typeDef", "int_split"],
    "稀有度": ["typeRarity", "int_split"],
    "是否是英雄": ["isHero", "number"],
    "魔力恢复速度": ["magicRecoverSp", "number"],
    "英雄单位攻击增加": ["atkIncrease", "number"],
    "英雄单位防御增加": ["defIncrease", "number"],
    "英雄单位生命增加": ["hpIncrease", "number"],
    "英雄单位回魔速度增加": ["MpIncreaseSp", "number"],
    "被击杀掉落魔力": ["BekillIncreaseMp", "number"],
    "被动技能": ["PassivesklsDec", "string"],
    "报到文本": ["unlockdes", "string"],
    "头像名称": "",
    "攻击范围": ""
}

config.items = {
    "ID":["id","number"],
    "名字":["name","string"],
    "说明":["desc","string"],
    "价格":["price","number"],
    "冷却时间": ""
}

config.achievements = {
    "ID": ["id", "number"],
    "成就名称": ["name", "string"],
    "成就描述": ["desc", "string"],
    "成就奖励": ["rewardstr", "string"],
    "成就类型": ["achType", "string"]
}

config.lvBarrack = {
    "等级": ["Level", "number"],
    "生命乘数": ["baselife", "number"],
    "攻击乘数": ["baseAtk", "number"],
    "防御乘数": ["basedefense", "number"],
    "费用乘数": ["basecost", "number"]
}

config.mactchLevel = {
    "id": ["id", "number"],
    "段位名称": ["name", "string"],
    "需要胜点": ["needwinPoint", "number"],
    "获胜奖励": ["winReward", "number"],
    "失败惩罚": ["failpunish", "number"],
    "段位奖励": ["BoxIds", "string"],
    "奖励数量": ["rewardNum", "number"],
    "赛季奖励": ["productIds", "string"],
    "段位铭牌": ["plateId", "string"],
    "结余胜点": ["surpluswinPoint", "number"]
}

config.manor = {
    "id": ["id", "number"],
    "领地名称": ["name", "string"],
    "领地说明": ["des", "string"],
    "生产力": ["creat", "string"],
    "领地类型": ["typeMr", "int_split"],
    "战斗增益": ["battleIncrease", "string"],
    "事件文本": ["actionDec", "string"],
    "事件选项": ["actionSelect", "string"],
    "选项文本": ["actionBtTx", "string"],
    "领地价格": ["costContain", "string"],
    "成功率": ["sucRate", "number"],
    "成功文本": ["sucDec", "string"],
    "失败文本": ["failDec", "string"],
    "解锁需通关关卡ID": ["needWinLvlID", "number"]
}

config.technology = {
    "id": ["id", "number"],
    "科技名称": ["name", "string"],
    "科技图标": ["iconId", "number"],
    "科技效果": ["des", "string"],
    "科技数值": ["valueTec", "string"],
    "基础消耗": ["baseCost", "number"],
    "最大等级": ["maxLv", "number"]
}

config.skills = {
    "id": ["id", "number"],
    "技能名称": ["name", "string"],
    "技能图标": ["iconId", "number"],
    "技能效果": ["des", "string"],
    "基础经验消耗": ["baseExpCost", "number"],
    "最大等级": ["maxLv", "number"],
    "训练速度": ["trainingSpd", "number"],
    "技能CD": ["skillCd", "number"],
    "MP消耗": ["MpCost", "number"],
    "数值类型": ["numtype", "number"],
    "显示数值": ["numstring", "string"]
}

config.towns = {
    "id": ["id", "number"],
    "雕像外观": ["iconId", "number"],
    "基础物资消耗": ["baseCost", "number"],
    "最大等级": ["maxLv", "number"],
    "生命值系数": ["hpcoff", "number"],
    "护甲值系数": ["defcoff", "number"],
    "生产速度系数": ["creatcoff", "number"],
    "初始金币": ["startgold", "number"],
    "十秒魔力": ["magictenseds", "number"],
    "十秒金币": ["goldtenseds", "number"],
    "攻击力": ["atkcoff", "number"],
    "伤害反射": ["hurtatkcoff", "number"],
    "防守增伤": ["defhurtcoff", "number"],
    "进攻增伤": ["atkhurtcoff", "number"]
}

config.goods = {
    "id": ["id", "number"],
    "物品名称": ["name", "string"],
    "物品图标": ["iconId", "number"],
    "物品说明": ["des", "string"],
    "物品类型": ["goodsType", "string"],
    "物品品质": ["quality", "number"],
    "售价": ["price", "number"]
}

config.awardboxs = {
    "id": ["id", "number"],
    "随机权重": ["quanzhong", "number"],
    "掉落类型,ID,数量": ["Award", "string"]
}

config.cards = {
    "id": ["id", "number"],
    "名称": ["name","string"],
    "抽卡消耗类型和数量": ["costStr", "string"],
    "抽取次数": ["useNum", "number"],
    "关联宝箱": ["boxid", "string"]
}

config.shops = {
    "id": ["id", "number"],
    "物品ID,数量": ["shopstr", "string"],
    "每日限购": ["daylimit", "number"],
    "折扣": ["discount", "number"],
    "商店类型": ["type", "number"],
    "金币价格": ["price", "number"]
}

config.heroLv = {
    "等级": ["Lv", "number"],
    "所需经验": ["needExp", "number"]
}

config.gamecontroll = {
    "id": ["id", "number"],
    "类型": ["type", "string"],
    "值": ["value", "number"],
    "说明": ["desc", "string"]
}

config.crisistgsdic = {
    "id": ["id", "number"],
    "危机类型": ["typename", "string"],
    "效果": ["eff", "string"],
    "描述": ["desc", "string"],
    "危机等级": ["level", "number"],
    "科技奖励": ["tec", "number"],
    "后勤消耗": ["costlogis", "number"]
}

config.plotsdic = {
    "id":["id","number"],
    "步骤": ["indexid","number"],
    "立绘资源":["standid","number"],
    "立绘位置":["algent","string"],
    "播放特效": ["effname","string"],
    "特效位置": ["effpos","string"],
    "是否抖动": ["isshake","number"],
    "入场效果": ["animname","string"],
    "效果翻转": ["isFilp","string"],
    "对话内容": ["content","string"],
}

config.equipdic = {
    "id": ["id", "number"],
    "装备名称": ["name", "string"],
    "最低品质": ["quality", "number"],
    "装备效果": ["des", "string"],
    "基础属性": ["baseproper", "number"],
    "限定英雄": ["limitheros", "string"],
    "出现权重": ["quanzhong", "number"]
}

config.pindutic = {
    "id": ["id", "number"],
    "绘卷插图": ["name", "string"],
    "奖励物品ID和数量": ["rewardstr", "string"],
    "阶段奖励": ["lastreward", "string"],
    "开始时间": ["startime", "string"],
    "结束时间": ["endtime", "string"]
}

config.constelldic = {
    "id":["id","number"],
    "星座名":["name","string"],
    "奖励物品id和数量":["rewardstr","string"],
    "激活文本":["des","string"]
}

const 指引 = {
    "id": "",
    "延迟时间": "",
    "指向目标": "",
    "指引文字": "",
    "是否暂停": "",
    "后续id": ""
}

const 任务等级 = {
    "任务等级": "",
    "需要经验": "",
    "奖励": ""
}

module.exports = config;