
CREATE TABLE stock (
    id SERIAL PRIMARY KEY,
    symbol TEXT NOT NULL,
    name TEXT NOT NULL,
    exchange TEXT NOT NULL,
    is_etf BOOLEAN NOT NULL
);

CREATE TABLE mention (
    stock_id INTEGER,
    dt TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    message TEXT NOT NULL,
    source TEXT NOT NULL,
    url TEXT NOT NULL,
    PRIMARY KEY (stock_id, dt),
    CONSTRAINT fk_mention_stock FOREIGN KEY (stock_id) REFERENCES stock (id)
);

CREATE INDEX ON mention (stock_id, dt DESC);
SELECT create_hypertable('mention', 'dt');

CREATE TABLE etf_holding (
    etf_id INTEGER NOT NULL, 
    holding_id INTEGER NOT NULL,
    dt DATE NOT NULL, 
    shares NUMERIC,
    weight NUMERIC, 
    PRIMARY KEY (etf_id, holding_id, dt),
    CONSTRAINT fk_etf FOREIGN KEY (etf_id) REFERENCES stock (id),
    CONSTRAINT fk_holding FOREIGN KEY (holding_id) REFERENCES stock (id)
);

CREATE TABLE stock_price (
    stock_id INTEGER NOT NULL,
    dt TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    open NUMERIC NOT NULL, 
    high NUMERIC NOT NULL,
    low NUMERIC NOT NULL,
    close NUMERIC NOT NULL, 
    volume NUMERIC NOT NULL,
    PRIMARY KEY (stock_id, dt),
    CONSTRAINT fk_stock FOREIGN KEY (stock_id) REFERENCES stock (id)
);

CREATE INDEX ON stock_price (stock_id, dt DESC);

SELECT create_hypertable('stock_price', 'dt');


SELECT count(*) as num_mentions, stock_id, symbol
from mention join stock on stock.id = mention.stock_id
group by stock_id, symbol, mention.dt
order by num_mentions DESC;



GAMESTOP
SELECT count(*), dt::date
from mention
group by count
order by dt DESC;


AMC
SELECT count(*), mention.dt::date
from mention
LEFT JOIN stock_price
on mention.stock_id = stock_price.stock_id
where mention.stock_id = 9136
group by mention.dt::date
order by dt DESC;

PLTR
SELECT count(*), mention.dt::date
from mention
LEFT JOIN stock_price
on mention.stock_id = stock_price.stock_id
where mention.stock_id = 10370
group by mention.dt::date
order by dt DESC;


SELECT count(*), mention.dt::date
from mention
LEFT JOIN stock_price
on mention.stock_id = stock_price.stock_id
where mention.stock_id = 9136
group by mention.dt::date
order by dt DESC;

select stock_id
from stock_price
where stock_id = 11033;



where stock_price.stock_id = 9136
group by dt::date;