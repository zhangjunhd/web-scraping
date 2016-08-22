# 查询目前记录数

    db.Fans.count() //Fans的记录数
    db.Follows.count() //Follows的记录数
    db.Information.count() // 用户信息数
    
    // map-reduce 算出总的uid数量
    map = function() {
    var max = 0;
    for (var key in this) {
        intKey = parseInt(key)
        if (intKey > max) {max = intKey} 
    }
    emit("tmp", max);
    }

    reduce = function(key, values) {
        var totalCount = 0;
        values.forEach(function(v){totalCount += v});
        return totalCount;
    }
    db.Fans.mapReduce(map, reduce, {out:"result"})
    db.result.find()

# 清理拓扑结果中无效数据
在Fans和Follows两个Collection中,凡是仅存在_id一条记录的,即仅存在主键的,说明爬取失败

    db.Fans.find({'1':{$exists: false}}).count() //Fans表无效记录数
    db.Follows.find({'1':{$exists: false}}).count() //Follows表无效记录数
    
    db.Fans.remove({'1':{$exists: false}})
    db.Follows.remove({'1':{$exists: false}})