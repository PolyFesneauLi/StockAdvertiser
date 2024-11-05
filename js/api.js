async function fetchData() {
    // 示例数据，可以替换为实际的API调用
    // const response = await fetch('path/to/your/api');
    // const data = await response.json();
    const data = generateMockData(100);

    // 假设数据格式为 { dates: ['2024-01-01', '2024-01-02', ...], prices: [100, 101, ...] }
    return {
        dates: data.dates,
        prices: data.prices
    };
}
function generateMockData(numPoints) {
    const dates = [];
    const prices = [];
    const startDate = new Date('2024-01-01');
    
    for (let i = 0; i < numPoints; i++) {
        const date = new Date(startDate);
        date.setDate(startDate.getDate() + i);
        dates.push(date.toISOString().split('T')[0]); // 格式化日期为 YYYY-MM-DD
        
        const price = 100 + Math.random() * 20; // 生成100到120之间的随机价格
        prices.push(price.toFixed(2)); // 保留两位小数
    }
    
    return { dates, prices };
}