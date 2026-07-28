-- Seed data for AGRO-BOT & AUTOMATION Database

-- Insert crop varieties
INSERT INTO crop_varieties (name, scientific_name, category, variety, season, growth_duration_days, water_requirement, soil_type_preference, temperature_range, spacing_cm, seed_rate_per_acre, expected_yield_per_acre, market_price_per_kg) VALUES
-- Cereals
('Rice', 'Oryza sativa', 'cereals', 'Basmati', 'kharif', 120, 'high', 'clay, loamy', '20-35°C', 20, 25, 2500, 45.0),
('Wheat', 'Triticum aestivum', 'cereals', 'Durum', 'rabi', 120, 'medium', 'loamy, sandy loam', '15-25°C', 15, 40, 3000, 25.0),
('Maize', 'Zea mays', 'cereals', 'Hybrid', 'kharif', 90, 'medium', 'well-drained loamy', '21-27°C', 75, 20, 4000, 20.0),
('Barley', 'Hordeum vulgare', 'cereals', 'Malting', 'rabi', 100, 'low', 'sandy loam', '12-22°C', 20, 35, 2000, 22.0),
('Millets', 'Pennisetum glaucum', 'cereals', 'Pearl', 'kharif', 75, 'low', 'sandy, drought resistant', '25-35°C', 10, 4, 1000, 35.0),

-- Vegetables
('Tomato', 'Solanum lycopersicum', 'vegetables', 'Hybrid', 'year_round', 90, 'medium', 'well-drained loamy', '20-25°C', 60, 200, 25000, 30.0),
('Potato', 'Solanum tuberosum', 'vegetables', 'Processing', 'rabi', 90, 'medium', 'sandy loam', '15-20°C', 60, 1500, 20000, 15.0),
('Onion', 'Allium cepa', 'vegetables', 'Red', 'rabi', 120, 'medium', 'well-drained loamy', '13-24°C', 15, 8, 15000, 25.0),
('Cabbage', 'Brassica oleracea', 'vegetables', 'Round', 'winter', 75, 'medium', 'fertile loamy', '15-20°C', 45, 300, 30000, 20.0),
('Cauliflower', 'Brassica oleracea var. botrytis', 'vegetables', 'Snowball', 'winter', 70, 'medium', 'rich loamy', '15-20°C', 45, 300, 25000, 35.0),

-- Pulses
('Chickpea', 'Cicer arietinum', 'pulses', 'Kabuli', 'rabi', 100, 'low', 'well-drained loamy', '20-25°C', 30, 40, 1200, 60.0),
('Lentil', 'Lens culinaris', 'pulses', 'Masoor', 'rabi', 95, 'low', 'loamy', '18-25°C', 25, 25, 800, 80.0),
('Black Gram', 'Vigna mungo', 'pulses', 'Urad', 'kharif', 75, 'medium', 'loamy', '25-30°C', 30, 15, 600, 90.0),
('Green Gram', 'Vigna radiata', 'pulses', 'Moong', 'summer', 65, 'medium', 'sandy loam', '25-30°C', 30, 15, 500, 85.0),
('Pigeon Pea', 'Cajanus cajan', 'pulses', 'Arhar', 'kharif', 180, 'low', 'well-drained', '20-30°C', 90, 12, 1000, 75.0),

-- Fruits
('Mango', 'Mangifera indica', 'fruits', 'Alphonso', 'year_round', 365, 'medium', 'well-drained deep', '24-27°C', 1000, 100, 8000, 150.0),
('Banana', 'Musa acuminata', 'fruits', 'Cavendish', 'year_round', 300, 'high', 'rich alluvial', '26-30°C', 200, 1600, 35000, 25.0),
('Apple', 'Malus domestica', 'fruits', 'Red Delicious', 'year_round', 365, 'medium', 'well-drained loamy', '10-24°C', 400, 250, 12000, 120.0),
('Orange', 'Citrus sinensis', 'fruits', 'Valencia', 'year_round', 365, 'medium', 'well-drained sandy loam', '13-37°C', 600, 400, 15000, 40.0),
('Grapes', 'Vitis vinifera', 'fruits', 'Thompson Seedless', 'year_round', 365, 'medium', 'well-drained loamy', '15-40°C', 300, 2000, 25000, 80.0),

-- Spices
('Turmeric', 'Curcuma longa', 'spices', 'Lakadong', 'kharif', 300, 'high', 'well-drained loamy', '20-30°C', 45, 2500, 8000, 180.0),
('Chili', 'Capsicum annuum', 'spices', 'Red Hot', 'kharif', 120, 'medium', 'well-drained loamy', '20-25°C', 45, 1, 1500, 120.0),
('Coriander', 'Coriandrum sativum', 'spices', 'Pant Haritma', 'rabi', 90, 'low', 'well-drained loamy', '20-25°C', 30, 12, 800, 200.0),
('Cumin', 'Cuminum cyminum', 'spices', 'Gujarat Cumin', 'rabi', 120, 'low', 'sandy loam', '25-30°C', 30, 8, 400, 400.0),
('Fenugreek', 'Trigonella foenum-graecum', 'spices', 'Kasuri Methi', 'rabi', 90, 'low', 'loamy', '15-25°C', 25, 20, 800, 150.0);

-- Insert marketplace categories
INSERT INTO marketplace_categories (name, description, image_url, sort_order) VALUES
('Fresh Produce', 'Fresh fruits and vegetables', '/images/categories/fresh-produce.jpg', 1),
('Grains & Cereals', 'Rice, wheat, maize and other grains', '/images/categories/grains.jpg', 2),
('Pulses & Legumes', 'Lentils, beans, chickpeas', '/images/categories/pulses.jpg', 3),
('Seeds & Saplings', 'Quality seeds and plant saplings', '/images/categories/seeds.jpg', 4),
('Fertilizers', 'Organic and chemical fertilizers', '/images/categories/fertilizers.jpg', 5),
('Pesticides', 'Pest control products', '/images/categories/pesticides.jpg', 6),
('Farm Equipment', 'Tractors, tools and machinery', '/images/categories/equipment.jpg', 7),
('Irrigation Supplies', 'Pipes, sprinklers, drip systems', '/images/categories/irrigation.jpg', 8),
('Livestock', 'Cattle, poultry, dairy products', '/images/categories/livestock.jpg', 9),
('Organic Products', 'Certified organic produce', '/images/categories/organic.jpg', 10);

-- Insert subcategories
INSERT INTO marketplace_categories (name, parent_category_id, description, sort_order) VALUES
-- Fresh Produce subcategories
('Vegetables', (SELECT id FROM marketplace_categories WHERE name = 'Fresh Produce'), 'Fresh vegetables', 1),
('Fruits', (SELECT id FROM marketplace_categories WHERE name = 'Fresh Produce'), 'Fresh fruits', 2),
('Herbs & Spices', (SELECT id FROM marketplace_categories WHERE name = 'Fresh Produce'), 'Fresh herbs and spices', 3),

-- Grains & Cereals subcategories
('Rice', (SELECT id FROM marketplace_categories WHERE name = 'Grains & Cereals'), 'All varieties of rice', 1),
('Wheat', (SELECT id FROM marketplace_categories WHERE name = 'Grains & Cereals'), 'Wheat and wheat products', 2),
('Maize', (SELECT id FROM marketplace_categories WHERE name = 'Grains & Cereals'), 'Corn and maize', 3),
('Millets', (SELECT id FROM marketplace_categories WHERE name = 'Grains & Cereals'), 'Traditional millets', 4);

-- Insert government schemes
INSERT INTO government_schemes (scheme_name, scheme_type, description, benefits, eligibility_criteria, required_documents, application_process, scheme_amount, percentage_subsidy, implementing_agency, state, is_active) VALUES
('Pradhan Mantri Kisan Samman Nidhi', 'grant', 'Direct income support to farmers', 'Rs. 6000 per year in three installments', 'Small and marginal farmers with cultivable land up to 2 hectares', 'Land records, Aadhaar card, Bank account details', 'Online application through PM-KISAN portal', 6000.00, 100.00, 'Ministry of Agriculture & Farmers Welfare', 'All States', true),

('Pradhan Mantri Fasal Bima Yojana', 'insurance', 'Crop insurance scheme for farmers', 'Comprehensive risk cover for crop loss', 'All farmers including sharecroppers and tenant farmers', 'Land records, Aadhaar card, Bank account, Sowing certificate', 'Through banks, insurance companies, or online', 200000.00, 95.00, 'Ministry of Agriculture & Farmers Welfare', 'All States', true),

('Soil Health Card Scheme', 'subsidy', 'Soil testing and health card for farmers', 'Free soil testing and nutrient recommendations', 'All farmers with agricultural land', 'Land ownership documents, Aadhaar card', 'Through agricultural extension centers', 0.00, 100.00, 'Department of Agriculture', 'All States', true),

('National Agriculture Market (e-NAM)', 'infrastructure', 'Online trading platform for agricultural commodities', 'Better price discovery and reduced transaction costs', 'All registered farmers and traders', 'Farmer registration, Quality certificates', 'Registration through e-NAM portal', 0.00, 0.00, 'Ministry of Agriculture & Farmers Welfare', 'All States', true),

('Pradhan Mantri Krishi Sinchai Yojana', 'subsidy', 'Irrigation development and water conservation', 'Financial assistance for irrigation infrastructure', 'Individual farmers, self-help groups, cooperatives', 'Land records, Project proposal, Bank account details', 'Through state agriculture departments', 500000.00, 75.00, 'Ministry of Agriculture & Farmers Welfare', 'All States', true),

('Kisan Credit Card', 'loan', 'Institutional credit support to farmers', 'Easy access to credit for agricultural needs', 'All farmers including tenant farmers', 'Land records, Aadhaar card, Income certificate', 'Through banks and cooperative societies', 300000.00, 0.00, 'NABARD', 'All States', true),

('National Mission for Sustainable Agriculture', 'grant', 'Sustainable agriculture practices promotion', 'Financial support for climate resilient practices', 'Progressive farmers and farmer groups', 'Land records, Group formation certificate', 'Through state implementing agencies', 100000.00, 60.00, 'Ministry of Agriculture & Farmers Welfare', 'All States', true),

('Rashtriya Krishi Vikas Yojana', 'grant', 'Agricultural development program', 'Infrastructure development and technology adoption', 'State governments and farmer producer organizations', 'Project proposal, Beneficiary identification', 'Through state planning departments', 1000000.00, 50.00, 'Planning Commission', 'All States', true),

('National Horticulture Mission', 'subsidy', 'Horticulture development program', 'Area expansion and productivity enhancement', 'Horticultural farmers and entrepreneurs', 'Land records, Technical feasibility report', 'Through horticulture departments', 250000.00, 85.00, 'Ministry of Agriculture & Farmers Welfare', 'All States', true),

('Paramparagat Krishi Vikas Yojana', 'subsidy', 'Organic farming promotion', 'Financial assistance for organic farming adoption', 'Farmers interested in organic farming', 'Land records, Group formation, Training certificate', 'Through organic farming clusters', 50000.00, 100.00, 'Ministry of Agriculture & Farmers Welfare', 'All States', true);

-- Log successful seed data insertion
DO $$
BEGIN
    RAISE NOTICE 'Seed data has been successfully inserted into AGRO-BOT & AUTOMATION database.';
    RAISE NOTICE 'Crop varieties: % records', (SELECT COUNT(*) FROM crop_varieties);
    RAISE NOTICE 'Marketplace categories: % records', (SELECT COUNT(*) FROM marketplace_categories);
    RAISE NOTICE 'Government schemes: % records', (SELECT COUNT(*) FROM government_schemes);
END
$$;