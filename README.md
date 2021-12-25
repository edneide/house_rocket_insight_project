# House Rocket - Insight Project

<p align="center">
  <img src="https://media.istockphoto.com/photos/home-for-sale-real-estate-sign-and-house-picture-id168769007?b=1&k=20&m=168769007&s=170667a&w=0&h=tUpO0uPn6vE4y-nI4hc770jraItM0rxUEi8YJuzM6q8="/>
</p>

This is an insight project where a data base from house sales in the King County (USA) was used to generate insights to help the CEO on making decisions about buying and selling properties. The *kc_house_data* can be found on [Kaggle](https://www.kaggle.com/harlfoxem/housesalesprediction). 

Here, you can find the final dashboard for this project: [House Rocket App](https://house-rocket-insightapp.herokuapp.com/)

Below, you can find the __dataset dictionary__.

**Variable** | **Meaning** 
--- | --- 
`id`  | Unique ID for each home sold
`date`| Date of the home sale
`price` | Price of each home sold
`bedrooms` | Number of bedrooms
`bathrooms` | Number of bathrooms, where .5 accounts for a room with a toilet but no shower
`sqft_living` | Square footage of the apartments interior living space
`sqft_lot` | Square footage of the land space
`floors` | Number of floors
`waterfront` | A dummy variable for whether the apartment was overlooking the waterfront or not
`view` | An index from 0 to 4 of how good the view of the property was
`condition` | An index from 1 to 5 on the condition of the apartment,
`grade` | An index from 1 to 13, where 1-3 falls short of building construction and design, 7 has an average level of construction and design, and 11-13 have a high quality level of construction and design.
`sqft_above` | The square footage of the interior housing space that is above ground level
`sqft_basement` | The square footage of the interior housing space that is below ground level
`yr_built` | The year the house was initially built
`yr_renovated` | The year of the house’s last renovation
`zipcode` | What zipcode area the house is in
`lat` | Lattitude
`long` | Longitude
`sqft_living15` | The square footage of interior housing living space for the nearest 15 neighbors
`sqft_lot15` | The square footage of the land lots of the nearest 15 neighbors


# Business question

We have two main questions:

1. What are the real states House Rocket should buy, and how much will it cost?
2. What is the best moment to sell the real states, and how much will it cost? 
    
# Business assumptions 

# Solution Planning

# Main business insights

- New houses are not substantially more expensive than old houses, on average. 
- Houses without basement are 22.56% bigger in total area than houses with basement.
- Waterfront houses are 212.64% more expensive, on average.
![](img/price_waterfront.png)

# Business results

## H1: Houses with waterfront are, on average, 30% more expensive.
**Conclusion**: False. Houses with waterfront are, on average, 212.64% more expensive. The mean price of houses without waterfront is U\$ 531,563.60, while this price is, on average, U\$ 1,661,876.025 for waterfront houses.

## H2: Houses built before 1955, are 50% cheaper, on average.

**Conclusion**: False. In average, "new" properties (year built >= 1955) are only 0.79% more expensive than the old ones (year built < 1955). The mean price of the old proporties is U$ 537,050.91 while the mean price of new properties is U$ 541,299.97.

## H3: Houses without basement have total area (sqft_lot) 40% bigger than houses with basement.

**Conclusion**: False. Although the proporties without basement are slightly bigger, they are only 22.56% bigger, not 40%. In average, properties without basement has area 16,284.18 square feet. Properties with basement has an area, in average, of 13,286.30 square feet.

## H4: The YoY (Year Over Year)  growth on houses price is 10%.

**Conclusion**: False. The YOY growth was only 0.52% between 2014 and 2015.

## H5: Houses with 3 bathrooms have a 15% MoM (Month over Month) price growth
**Conclusion**: False. The average MoM price growth was only 0.375%.


# Conclusion

If the houses are sold by the suggested price, the expected total profit would be U$ 760,693,197.90. 
   
# Next Steps

- Explore the possibility to renovate the house and sell them.
- Explore models to predict houses prices based on some features. 

