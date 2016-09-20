# 列出所有的分类

    db.Site.distinct("type")

# 列出分类下的子类类目

    db.Site.aggregate([
        {$match:{'type': '购物网站'}},
        {$group:{_id:"$subtype"}}
    ])

# 统计各个分类中的网站数量

    db.Site.aggregate([{$group:{_id:"$type", count:{$sum:1}}}])

# 统计某个分类下子分类的网站数量

    db.Site.aggregate([
        {$match:{'type': '政府组织'}},
        {$group:{_id:"$subtype", count:{$sum:1}}}
    ])

# 排序某个子分类
    db.Site.find({"subtype":"电商网站", "region_rank":{$ne:0}}).sort({"region_rank":1})

# rank缺失值填充
## 打印所有region_rank为null的记录

    db.getCollection('Site').find({"region_rank":null})
    db.getCollection('Site').find({"region_rank":null}).count()

## 将region_rank为null的记录更新为0

    db.Site.find({"region_rank":null}).forEach(function(x){
        x.region_rank = 0;
        db.Site.save(x);
        print(x._id);
    })

## 验证

    db.getCollection('Site').find({"region_rank":0})
