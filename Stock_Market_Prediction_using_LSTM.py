# LSTM project
{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyOnYReJ57ekekrxe6lgk/4a",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/Ashwin2708/Stock-Market-Prediction-using-LSTM/blob/main/Stock_Market_Prediction_using_LSTM.ipynb\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "#First we import the libraries to support our program\n",
        "import math\n",
        "import pandas_datareader as web\n",
        "import numpy as np\n",
        "import pandas as pd\n",
        "from sklearn.preprocessing import MinMaxScaler\n",
        "from keras.models import Sequential\n",
        "from keras.layers import Dense, LSTM\n",
        "import matplotlib.pyplot as plt\n",
        "plt.style.use('fivethirtyeight')\n",
        "!pip install --upgrade pandas-datareader"
      ],
      "metadata": {
        "id": "DloKBS7kzDMN",
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "outputId": "7778c675-35cc-4b28-aa15-fea0bec18366"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Looking in indexes: https://pypi.org/simple, https://us-python.pkg.dev/colab-wheels/public/simple/\n",
            "Requirement already satisfied: pandas-datareader in /usr/local/lib/python3.7/dist-packages (0.10.0)\n",
            "Requirement already satisfied: lxml in /usr/local/lib/python3.7/dist-packages (from pandas-datareader) (4.9.1)\n",
            "Requirement already satisfied: requests>=2.19.0 in /usr/local/lib/python3.7/dist-packages (from pandas-datareader) (2.23.0)\n",
            "Requirement already satisfied: pandas>=0.23 in /usr/local/lib/python3.7/dist-packages (from pandas-datareader) (1.3.5)\n",
            "Requirement already satisfied: python-dateutil>=2.7.3 in /usr/local/lib/python3.7/dist-packages (from pandas>=0.23->pandas-datareader) (2.8.2)\n",
            "Requirement already satisfied: pytz>=2017.3 in /usr/local/lib/python3.7/dist-packages (from pandas>=0.23->pandas-datareader) (2022.2.1)\n",
            "Requirement already satisfied: numpy>=1.17.3 in /usr/local/lib/python3.7/dist-packages (from pandas>=0.23->pandas-datareader) (1.21.6)\n",
            "Requirement already satisfied: six>=1.5 in /usr/local/lib/python3.7/dist-packages (from python-dateutil>=2.7.3->pandas>=0.23->pandas-datareader) (1.15.0)\n",
            "Requirement already satisfied: chardet<4,>=3.0.2 in /usr/local/lib/python3.7/dist-packages (from requests>=2.19.0->pandas-datareader) (3.0.4)\n",
            "Requirement already satisfied: certifi>=2017.4.17 in /usr/local/lib/python3.7/dist-packages (from requests>=2.19.0->pandas-datareader) (2022.6.15)\n",
            "Requirement already satisfied: idna<3,>=2.5 in /usr/local/lib/python3.7/dist-packages (from requests>=2.19.0->pandas-datareader) (2.10)\n",
            "Requirement already satisfied: urllib3!=1.25.0,!=1.25.1,<1.26,>=1.21.1 in /usr/local/lib/python3.7/dist-packages (from requests>=2.19.0->pandas-datareader) (1.24.3)\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "#Get the stock quote\n",
        "df = web.DataReader('AAPL', data_source='yahoo', start='2012-01-01', end='2019-12-31')\n",
        "#show the data\n",
        "df"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 455
        },
        "id": "0DVtJl8Q0LOI",
        "outputId": "c09e4918-5b71-4891-ff32-773b9fe8ecc9"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "                 High        Low       Open      Close       Volume  Adj Close\n",
              "Date                                                                          \n",
              "2012-01-03  14.732143  14.607143  14.621429  14.686786  302220800.0  12.540045\n",
              "2012-01-04  14.810000  14.617143  14.642857  14.765714  260022000.0  12.607436\n",
              "2012-01-05  14.948214  14.738214  14.819643  14.929643  271269600.0  12.747406\n",
              "2012-01-06  15.098214  14.972143  14.991786  15.085714  318292800.0  12.880664\n",
              "2012-01-09  15.276786  15.048214  15.196429  15.061786  394024400.0  12.860233\n",
              "...               ...        ...        ...        ...          ...        ...\n",
              "2019-12-24  71.222504  70.730003  71.172501  71.067497   48478800.0  69.738731\n",
              "2019-12-26  72.495003  71.175003  71.205002  72.477501   93121200.0  71.122368\n",
              "2019-12-27  73.492500  72.029999  72.779999  72.449997  146266000.0  71.095390\n",
              "2019-12-30  73.172501  71.305000  72.364998  72.879997  144114400.0  71.517342\n",
              "2019-12-31  73.419998  72.379997  72.482498  73.412498  100805600.0  72.039879\n",
              "\n",
              "[2012 rows x 6 columns]"
            ],
            "text/html": [
              "\n",
              "  <div id=\"df-3cce0055-be7b-4e8c-998d-445a74af9e52\">\n",
              "    <div class=\"colab-df-container\">\n",
              "      <div>\n",
              "<style scoped>\n",
              "    .dataframe tbody tr th:only-of-type {\n",
              "        vertical-align: middle;\n",
              "    }\n",
              "\n",
              "    .dataframe tbody tr th {\n",
              "        vertical-align: top;\n",
              "    }\n",
              "\n",
              "    .dataframe thead th {\n",
              "        text-align: right;\n",
              "    }\n",
              "</style>\n",
              "<table border=\"1\" class=\"dataframe\">\n",
              "  <thead>\n",
              "    <tr style=\"text-align: right;\">\n",
              "      <th></th>\n",
              "      <th>High</th>\n",
              "      <th>Low</th>\n",
              "      <th>Open</th>\n",
              "      <th>Close</th>\n",
              "      <th>Volume</th>\n",
              "      <th>Adj Close</th>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>Date</th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "    </tr>\n",
              "  </thead>\n",
              "  <tbody>\n",
              "    <tr>\n",
              "      <th>2012-01-03</th>\n",
              "      <td>14.732143</td>\n",
              "      <td>14.607143</td>\n",
              "      <td>14.621429</td>\n",
              "      <td>14.686786</td>\n",
              "      <td>302220800.0</td>\n",
              "      <td>12.540045</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>2012-01-04</th>\n",
              "      <td>14.810000</td>\n",
              "      <td>14.617143</td>\n",
              "      <td>14.642857</td>\n",
              "      <td>14.765714</td>\n",
              "      <td>260022000.0</td>\n",
              "      <td>12.607436</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>2012-01-05</th>\n",
              "      <td>14.948214</td>\n",
              "      <td>14.738214</td>\n",
              "      <td>14.819643</td>\n",
              "      <td>14.929643</td>\n",
              "      <td>271269600.0</td>\n",
              "      <td>12.747406</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>2012-01-06</th>\n",
              "      <td>15.098214</td>\n",
              "      <td>14.972143</td>\n",
              "      <td>14.991786</td>\n",
              "      <td>15.085714</td>\n",
              "      <td>318292800.0</td>\n",
              "      <td>12.880664</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>2012-01-09</th>\n",
              "      <td>15.276786</td>\n",
              "      <td>15.048214</td>\n",
              "      <td>15.196429</td>\n",
              "      <td>15.061786</td>\n",
              "      <td>394024400.0</td>\n",
              "      <td>12.860233</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>...</th>\n",
              "      <td>...</td>\n",
              "      <td>...</td>\n",
              "      <td>...</td>\n",
              "      <td>...</td>\n",
              "      <td>...</td>\n",
              "      <td>...</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>2019-12-24</th>\n",
              "      <td>71.222504</td>\n",
              "      <td>70.730003</td>\n",
              "      <td>71.172501</td>\n",
              "      <td>71.067497</td>\n",
              "      <td>48478800.0</td>\n",
              "      <td>69.738731</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>2019-12-26</th>\n",
              "      <td>72.495003</td>\n",
              "      <td>71.175003</td>\n",
              "      <td>71.205002</td>\n",
              "      <td>72.477501</td>\n",
              "      <td>93121200.0</td>\n",
              "      <td>71.122368</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>2019-12-27</th>\n",
              "      <td>73.492500</td>\n",
              "      <td>72.029999</td>\n",
              "      <td>72.779999</td>\n",
              "      <td>72.449997</td>\n",
              "      <td>146266000.0</td>\n",
              "      <td>71.095390</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>2019-12-30</th>\n",
              "      <td>73.172501</td>\n",
              "      <td>71.305000</td>\n",
              "      <td>72.364998</td>\n",
              "      <td>72.879997</td>\n",
              "      <td>144114400.0</td>\n",
              "      <td>71.517342</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>2019-12-31</th>\n",
              "      <td>73.419998</td>\n",
              "      <td>72.379997</td>\n",
              "      <td>72.482498</td>\n",
              "      <td>73.412498</td>\n",
              "      <td>100805600.0</td>\n",
              "      <td>72.039879</td>\n",
              "    </tr>\n",
              "  </tbody>\n",
              "</table>\n",
              "<p>2012 rows × 6 columns</p>\n",
              "</div>\n",
              "      <button class=\"colab-df-convert\" onclick=\"convertToInteractive('df-3cce0055-be7b-4e8c-998d-445a74af9e52')\"\n",
              "              title=\"Convert this dataframe to an interactive table.\"\n",
              "              style=\"display:none;\">\n",
              "        \n",
              "  <svg xmlns=\"http://www.w3.org/2000/svg\" height=\"24px\"viewBox=\"0 0 24 24\"\n",
              "       width=\"24px\">\n",
              "    <path d=\"M0 0h24v24H0V0z\" fill=\"none\"/>\n",
              "    <path d=\"M18.56 5.44l.94 2.06.94-2.06 2.06-.94-2.06-.94-.94-2.06-.94 2.06-2.06.94zm-11 1L8.5 8.5l.94-2.06 2.06-.94-2.06-.94L8.5 2.5l-.94 2.06-2.06.94zm10 10l.94 2.06.94-2.06 2.06-.94-2.06-.94-.94-2.06-.94 2.06-2.06.94z\"/><path d=\"M17.41 7.96l-1.37-1.37c-.4-.4-.92-.59-1.43-.59-.52 0-1.04.2-1.43.59L10.3 9.45l-7.72 7.72c-.78.78-.78 2.05 0 2.83L4 21.41c.39.39.9.59 1.41.59.51 0 1.02-.2 1.41-.59l7.78-7.78 2.81-2.81c.8-.78.8-2.07 0-2.86zM5.41 20L4 18.59l7.72-7.72 1.47 1.35L5.41 20z\"/>\n",
              "  </svg>\n",
              "      </button>\n",
              "      \n",
              "  <style>\n",
              "    .colab-df-container {\n",
              "      display:flex;\n",
              "      flex-wrap:wrap;\n",
              "      gap: 12px;\n",
              "    }\n",
              "\n",
              "    .colab-df-convert {\n",
              "      background-color: #E8F0FE;\n",
              "      border: none;\n",
              "      border-radius: 50%;\n",
              "      cursor: pointer;\n",
              "      display: none;\n",
              "      fill: #1967D2;\n",
              "      height: 32px;\n",
              "      padding: 0 0 0 0;\n",
              "      width: 32px;\n",
              "    }\n",
              "\n",
              "    .colab-df-convert:hover {\n",
              "      background-color: #E2EBFA;\n",
              "      box-shadow: 0px 1px 2px rgba(60, 64, 67, 0.3), 0px 1px 3px 1px rgba(60, 64, 67, 0.15);\n",
              "      fill: #174EA6;\n",
              "    }\n",
              "\n",
              "    [theme=dark] .colab-df-convert {\n",
              "      background-color: #3B4455;\n",
              "      fill: #D2E3FC;\n",
              "    }\n",
              "\n",
              "    [theme=dark] .colab-df-convert:hover {\n",
              "      background-color: #434B5C;\n",
              "      box-shadow: 0px 1px 3px 1px rgba(0, 0, 0, 0.15);\n",
              "      filter: drop-shadow(0px 1px 2px rgba(0, 0, 0, 0.3));\n",
              "      fill: #FFFFFF;\n",
              "    }\n",
              "  </style>\n",
              "\n",
              "      <script>\n",
              "        const buttonEl =\n",
              "          document.querySelector('#df-3cce0055-be7b-4e8c-998d-445a74af9e52 button.colab-df-convert');\n",
              "        buttonEl.style.display =\n",
              "          google.colab.kernel.accessAllowed ? 'block' : 'none';\n",
              "\n",
              "        async function convertToInteractive(key) {\n",
              "          const element = document.querySelector('#df-3cce0055-be7b-4e8c-998d-445a74af9e52');\n",
              "          const dataTable =\n",
              "            await google.colab.kernel.invokeFunction('convertToInteractive',\n",
              "                                                     [key], {});\n",
              "          if (!dataTable) return;\n",
              "\n",
              "          const docLinkHtml = 'Like what you see? Visit the ' +\n",
              "            '<a target=\"_blank\" href=https://colab.research.google.com/notebooks/data_table.ipynb>data table notebook</a>'\n",
              "            + ' to learn more about interactive tables.';\n",
              "          element.innerHTML = '';\n",
              "          dataTable['output_type'] = 'display_data';\n",
              "          await google.colab.output.renderOutput(dataTable, element);\n",
              "          const docLink = document.createElement('div');\n",
              "          docLink.innerHTML = docLinkHtml;\n",
              "          element.appendChild(docLink);\n",
              "        }\n",
              "      </script>\n",
              "    </div>\n",
              "  </div>\n",
              "  "
            ]
          },
          "metadata": {},
          "execution_count": 5
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "#Get the number of rows and colums in the data set\n",
        "df.shape"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "PsuSMfhz2aLP",
        "outputId": "ca2e98df-fd82-4ad6-b481-097d143c38d9"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "(2012, 6)"
            ]
          },
          "metadata": {},
          "execution_count": 6
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "#Visualize the closing price hsitory\n",
        "plt.figure(figsize=(16,8))\n",
        "plt.title(\"Close Price History\")\n",
        "plt.plot(df['Close'])\n",
        "plt.xlabel('Date', fontsize=18)\n",
        "plt.ylabel('Closing Price USD ($)', fontsize=18)\n",
        "plt.show()"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 558
        },
        "id": "8iqUeI_T2rfK",
        "outputId": "00fedcd3-7659-42a1-cd49-bffad5a25861"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "display_data",
          "data": {
            "text/plain": [
              "<Figure size 1152x576 with 1 Axes>"
            ],
            "image/png": "iVBORw0KGgoAAAANSUhEUgAABCMAAAIdCAYAAAAH77cvAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAALEgAACxIB0t1+/AAAADh0RVh0U29mdHdhcmUAbWF0cGxvdGxpYiB2ZXJzaW9uMy4yLjIsIGh0dHA6Ly9tYXRwbG90bGliLm9yZy+WH4yJAAAgAElEQVR4nOzdd3RUdf7/8dekh1RKCBC6hLZUQRCwfRVFBKWIoqiroMuKXdQVvmtZsQCi/HRdZWVdrID9i4CAIiIdxAIivUgNhCSk18nM/P6IiUzNTDIlGZ6PczjHuffOnc+dC8dzX/P+vD+GnJwciwAAAAAAAPwkJNADAAAAAAAA5xbCCAAAAAAA4FeEEQAAAAAAwK8IIwAAAAAAgF8RRgAAAAAAAL8ijAAAAAAAAH5FGAEAgA8cOXJEiYmJmjRpUqCHUidMmjRJiYmJOnLkSKCHUmuJiYkaNmxYoIcBAEC9RhgBAICb9u/fr8cff1wDBw5U69atlZSUpI4dO2rMmDGaN2+eCgsLAz1Erxk2bJgSExOt/qSkpGjgwIF69tlnlZOTE+gh1lhlUNS9e3eXx3Xv3t3rAUrlZxNmAADOdWGBHgAAAPXBiy++qBkzZshsNqtv37666aabFBcXp9OnT2vjxo2aPHmyXnvtNf3888+BHqpX3XzzzWrdurUsFovS09O1fPlyvfzyy1q0aJFWrVqlxMREt87z9NNP6+GHH1aLFi18PGLf+/777xUdHR3oYQAAUK8RRgAAUI2XX35ZL7zwglJSUvT222+rX79+dsesXr1azz33XABG51vjxo3TxRdfXPX6ueee0+DBg7V3717NnTtXf/vb39w6T7NmzdSsWTNfDdOvOnbsGOghAABQ7zFNAwAAF44cOaIZM2YoPDxcH330kcMgQpL+53/+R8uWLXPrnKdPn9bf/vY39ezZU02bNlW7du00duxYbdiwwe5Yi8WihQsXasiQIerQoYOSk5PVtWtXXXvttXr33Xftjs/NzdXzzz+vAQMGqHnz5mrZsqWuvvpqLVq0yLMLdyIuLk7jxo2TJP34449V2yunPeTm5mrKlCnq1q2bGjdurDfeeEOS654RP/30kyZMmKAuXbpUTX259tprtWDBArtjt23bpgkTJqhz585KSkpSp06dNHHiRB06dMgr1+cOR9Ms8vPzNWvWrKopPCkpKerRo4duvfVWrVu3TpI0f/589ezZU5K0YcMGqykw06dPtzrf4sWLNXz4cLVu3VrJycnq16+fnn/+eRUUFNiNp3JKzeHDhzVnzhwNGDBAycnJGjdunN5++20lJiZqxowZDq8lJydHzZs3V7du3WQ2m73x9QAA4BYqIwAAcGH+/PkyGo0aPXq0unXr5vLYyMjIas939OhRDR06VCdOnNCgQYM0evRonTp1SosWLdLKlSv12muv6ZZbbqk6/tlnn9Xs2bPVunVrjRgxQgkJCUpPT9evv/6qDz/8ULfffnvVsWlpabr22mt18OBBDRgwQHfccYeKior09ddf64477tDjjz+uqVOn1vzL+J3FYnG4vaysTNddd51yc3N15ZVXKjo6WikpKS7P9d577+nhhx9WSEiIrr76aqWmpiorK0vbt2/XnDlzqoIPSfr44491zz33KCIiQkOHDlVKSooOHTqkzz77TCtWrNDSpUvVo0ePWl+fpywWi8aMGaMtW7aoT58+uuWWWxQREaGTJ09q48aNWrNmjS6++GJ1795dd999t/7973+rVatWVtd20UUXVf33888/r1mzZqlhw4YaPXq0EhIStHr1as2aNUvLly/X8uXLFRcXZzeOxx9/XJs3b9aQIUN01VVXKTY2VjfccIOefvppvf/++3rssccUGhpq9Z6FCxequLhYt99+u0JC+I0KAOA/hBEAALiwefNmSdJll13mlfNNnjxZJ06c0JQpUzRlypSq7ffdd58GDx6syZMn67LLLqt6iH/77bfVvHlzbdq0STExMVbnysrKsno9adIkHTp0SG+99ZbGjBlTtT0vL0/Dhw/Xiy++qOHDh1fbuNGV/Pz8qoqFvn37Wu1LT09Xly5dtHz5cjVo0KDac+3Zs0eTJ09WTEyMli9frj/96U9W+48fP17134cOHdL999+vli1batmyZVa9J9atW6eRI0fq/vvv15o1a9y+ltzcXLuKBNv97ti1a5e2bNmia665xq6aw2KxKDs7W5LUo0cPJSQk6N///rdat27tMBjaunWrZs2apRYtWmjVqlVq3ry5JOkf//iHJk2apA8//FDTpk3TrFmz7N77yy+/aO3atWrTpo3V9rFjx+o///mPvvrqK11zzTVW+9555x2FhYXptttuc+taAQDwFsIIAABcSE9PlySvNF5MS0vTN998o5SUFE2ePNlq35/+9CdNmDBBr7/+uj766COr/eHh4QoLs/9fduPGjav+e+fOnVqzZo2GDx9uFURIUnx8vKZMmaJx48bpk08+8SiMWLBggdavX1/VwHLFihVKT09X+/bt9Ze//MXu+GeffdatIEKS/vvf/6q8vFyPPvqoXRAhSS1btrQ6trS0VC+88ILdvbj44os1dOhQLV26VHv27FHnzp3d+vy8vDzNnDnTrWPd4aippcFgUKNGjdw+x/vvvy+pIrSqDCIqzzNt2jR98cUXWrBggV544QWFh4dbvfeBBx6wCyIk6c4779R//vMfvfPOO1ZhxIYNG7R3715dd911QdPPAwBQfxBGAADgJ9u3b5ck9e/fXxEREXb7L7vsMr3++utVx0nSDTfcoLlz56pfv34aOXKkBgwYoP79+6thw4ZW792yZYukisoFR7/2V1ZR7N2716MxL1y4sOq/GzRooLZt2+qWW27RAw88YLeSRlRUVLVTWc72ww8/SJIGDx5c7bGV17dx40ar76dSRkaGpIrrczeMaNWqlXbs2OF0f/fu3XXs2LFqz9O5c2d1795dn332mY4ePaprrrlG/fv31/nnn6+oqCi3xlKp8touueQSu31NmzZV165d9eOPP+rAgQPq0qWL1f4+ffo4Hd+gQYP0zTff6NixY2rVqpWkiqoISZowYYJHYwQAwBsIIwAAcCE5OVl79+5VWlparc+Vl5cnqeKh0tlnSdbTA6ZPn6727dtrwYIF+uc//6lXX31VISEhuvTSSzVt2rSqKoczZ85IktasWeNyqkJhYaFHY16yZInVahquNGnSRAaDwe1zV16nO1Unldf3r3/9y+Vxnl6fN4SGhmrJkiWaNWuWFi9erGeeeUZSRXgzatQoTZs2zaqKxZWa/B2p5Ow9knTXXXdpw4YNevfdd/XEE08oKytLixcv1nnnnadLL73UrbEBAOBNdCoCAMCFCy+8UJI86kXgTHx8vKSK1TQcqZwSUnmcVPGge/fdd2vt2rU6ePCgFixYoBtvvFHfffedRo0aVfWQXvme5557Tjk5OU7/LF26tNbX4YwnQYQkJSQkSJJbQU/l9f32228ur+/sppD+lJiYqOeff147duzQtm3b9MYbb6hXr16aP3++7rjjDrfPU5O/I5Vcff/Dhw9Xs2bN9MEHH6i8vFwLFixQaWmp7rjjDo/vGwAA3kAYAQCAC7fccovCw8O1ePFi7dq1y+WxpaWlLvdXrvSwZcsWlZWV2e2vDDx69erl8P2NGjXSNddco3//+9+6/vrrlZmZqU2bNklS1ZKjla/rg8oGmN988021x15wwQWSKqZp1HVt27bVuHHjtHjxYrVs2VLr1q2rqmSoXM3C2TKalUt/Vi4HeraMjAzt3r1bMTExSk1N9WhM4eHhuu2223Tq1Cl9+eWXeueddxQZGWm1cgsAAP5EGAEAgAtt2rTRlClTZDQadeONN1b1ObC1du1aDR8+3OW5UlJSdMUVV+jEiRN69dVXrfbt3r1b8+bNU2RkpG688UZJFeGGo3DBYrFU9UiobBbZq1cvDRo0SMuWLdO7777rcPnNAwcOuNUDwV/uvPNOhYWF6aWXXnIY9Jw4caLqvydOnKiIiAg98cQT2rdvn92x5eXlWrt2rU/H68zhw4d1+PBhu+0FBQUqLCy0akCamJgog8FgtVLI2W699VZJ0uzZs6uqIKSKe/7000+rqKhIN998s13zSneMHz9eoaGhmjp1qg4ePKgRI0Z41FwTAABvomcEAADVeOSRR1ReXq6ZM2dq8ODB6tevn3r37q24uDhlZGRo8+bN2rt3r84777xqzzV79mxdffXVev7557V27VpdcMEFOnXqlBYtWqSSkhK98sorVatIFBcXa+jQoWrbtq169+6tVq1ayWg0av369dqxY4cuuOACq34Ob731lkaMGKEHH3xQb775pi644AI1bNhQaWlp2rNnj3755Rd98MEHVQ0MA61z5856+eWX9fDDD+uyyy7T1VdfrdTUVGVnZ+uXX35RaWlpVYVAamqq3njjDd17770aMGCABg8erPPOO08mk0knTpzQli1bVFpaqqNHj/r9On799Vfddttt6tWrlzp16qTmzZsrJydHX331lbKzs3XfffdVLcsaGxurfv36acuWLRo7dqx69uyp8PBwDRw4UIMGDVK/fv00efJkzZ49WwMGDNDIkSMVHx+v1atXa/v27erataueeuqpGo2zRYsWVauOSBXhBAAAgUIYAQCAGx5//HGNGjVKb731ltavX6+FCxeqqKhIDRs2VLdu3TRx4kTdfPPN1Z6nTZs2+u677/TSSy9pxYoV2rx5s2JiYjRo0CA98MADVuFCTEyMpk2bpnXr1mnr1q1avny5oqOj1aZNGz33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tEqOi/nWaUm+HgKGRXB5FBERERFRTTAY0QCUmkVM+sl+N4dB4dUvrkjVF6KUY24f67oS0+74Vjwjwzplvzwft6YTMLqQV/XOErdcKzQjp9iMU7pSDAlXwNtdgMEkYu91Az48aR28eCxW+vayA0IVuJhvnfUysplnrZeAEBERERE1VQxGNADbL9vPivh0qH+tugSQcwVU0D6yVJTwQurY2RvVD0ZsOF+I94/rK/05BShkddLdJbmbCgezDDiXZ4K7DLg/Wom3Kih6SkREREREFWMwogE4rrVta7hkoBr3t2zcLTcbmkCF42CE0dx0ohEX862DESp3AfnGise/+LgeVfkRvd3HD8o6yDKJUrnhl8RQnNSWorWvGzybUKYLEREREZErsJtGA6ApNlv9fUp7bzxaB6nqVLGKMiOMN6dQFEWsP1eIf/xPi5+u1axdZX2nNVh/Xv/WtvLPalUCEZPaeuGvresuACcTBHQKcGcggoiIiIjICRiMaADKP9x1D2xaxRAbCi83GXoF25+b0ptP20uO6/HkXi1Wni3Efds1OKuzzXpp6MpnQYR4yrCwv7rWx62LWhFEREREROQaDEY0ALnlghEVfQNPdWv5kACMj1GifIMToxk4pTXi9cN5Vtu3O+iS0pDllVh/XlUeMkxq542LD4Vj2SB/rBjij7+2ql63ixCljK0viYiIiIgaEdaMaAAu661bCoY4aIFIdS9a5YblQwJwb1QRHt2da9luNJctzyjvfA06T9RXBzMNeHqfFufyrD+vKveyyIxaIbMss7BXB8WRZl5yvNvfD24yLo8gIiIiImosGIyo50pMos0Days/Tlt9514ueaVUBNJzbR/APz1TiLf7qCssyiiKIg5kleBwVgnuClege1DV2rmKooitfxTjjK4UD8QoEaVy3ecm32jGw7tykVOuvgkAqMr/MACc1FYehOkf6oEvhgfC10Ng1xgiIiIiokaGT7X13IYLRVbtDiO8ZPDz4DKN+q78t/hZRSbk2nlQB4C7v8vGtjHBdgMSJSYRf/spF9/9Ubacw00AttwdhP6hikqv4YEdGuy8agAArDitx6/jwlzWieKDE3q7gQgA8POwPefYKE9876BlbUofPzwa6wUvNwECgxBERERERI0Sn2rrse2XizE1VWu1rSoPoVT3yicD/JZjxKVyy21uOaox4h8/a+2+NvdIniUQAZRlWMxPy6/0/Mc0JZZABABcKzTjs7MFVbjymlmdYbsEBSgLnrT3t631MCrS0+Gxklop4e0uYyCCiIiIiKgRYzCinsosNCFpp8Zqm4Cytp5U/1W3vsH6c0U22368WozFx/U229M0lddb+NxOcCD54A18f7nsPKIoYvfVYnx0Uo+jOSWWbh818Wt2iU1dk1va+LnB104mT7BSjkdjbdt0Dgj1QABrohARERERNXoMRtRTbx3Js9n2eDtv9GNmRIPgXoMv9dWfXsUxTYnl7wuO2c+AyCk2Q2+0vyQCAExmEV9fsA1uAMDCY2XBjYXpetz/gwYvH7yBoVuyMWJrNnKL7QcUKjPpp1yHrw2NcPx5HdfSNhgxKJyfbyIiIiKipoDBiHro0V0arLHzzfbznX3q4GqoJjzK9/YsJyHa/jKFcT9oUFwqIrfYhJ//LLG7DwBcynccODiYVYJsB/UbDmaV4OEfNXjrV+tg11GNEfMdBD8qYjSLDmtFeMqBJzs4/sz2DrFdvtHBzpIOIiIiIiJqfBiMqGd0BjM2X7It7Pf16EA092G90YbCX1HxrXVPCyWa+9guR8guNmPn1WLsuGpARQsnLuY77kYxZltOhef+9g/7hSM/OFGAqwVVz44QRRH3fJeDwlLrK/1brBdGRSrw6dAARFfQwcPLTYYxLW4HZfw8BAxhZgQRERERUZPAp9t65s8i24fBlUMDMDTCccE/qn/CvSque+DjLuClrio8/z+dzWvLTuqxr4KsCAA4rjWiR7AHDmQa0DvYA5E3A1VndZXXk6hIx//+iU2jAhHXrPLP20enCnAo2/o6H2njhUUD/at8vnl9/QAAfxaakNzNF+pKgjhERERERNQ4MBhRzxQYbb8Pv9dBSj/VXwq5gAgvGa4V2i5hUMoF9AvxgL9ChtTrBnx53rq+g71AxIhmCqvuGCm/5SPlt7JlFd5uAr4aFYj+oQqc0NoGI7zcBJvshYrc/4MGc/v4YWoHb8gcdLQ4n1eK5IM3bLbP7O5b5fMAQHMfN6wdHlit9xARERERUcPHryHrkd1Xi/HgDusOGgNCPRw+EFL99lCb251PugW6I7GlEt2D3LFssD8CPOUQBAEfDwnAskGVZxI82cEHbg4+BgWlImbeDAzkGmyDH/52ullU5pVDN/B0qm27UZ3BjHE/5KDHhkyb1/oEeyDCm50wiIiIiIiocsyMqAdyik04pjFiwo8aGMqt0lDVpC0D1QuzuqvQJcAdeqMZY1ooHS5BuC9aiafsPPjfqUuAO4ZHemL7Zfv1Ho5qjJi0OxfRKutgwITWXvjid9tiqJtGBaJXiAcA4NVDN7DqrO0+688V4e0+JkurzZ//NFRYj2JeP78Kx0BERERERHQLgxF1aEe2HL33Xa1wn5M6x4UKqX6TCQLujVZWup+nm4CWKjkuOOiQ0cJHjhClDA/GKB0GIwBg00Xbdp4DwzwQ6S3Hu2m3O2Uo5LCqCbF4oD+ClXLMT7PupiECOK0rRbiXiPXnCvHO0Yq7bQSw3gMREREREVURnx7qSGGpGXN/96h0v8v6qnc3oIbrvgqCFrO6+0K4GdjwcbRWw4G4CE/8tZUXAm8GClTuAk4nhdvs90p3Fca1tL2GPdcNGP1ddqWBCADwq8FyECIiIiIiapqYGVFH9meWoMBU+YPlxDZeElwN1bXxMV5YmK632vZqD18MjVCgV3BZ0MpdJuDCw+EIXnWtSsfsoHZDs5s1HA4mhuCkthQ9g9zh7W4bNBAEAZ8MDUCsOs9SGBMA5lUhCHELlxQREREREVFV8avMOrLziuN0+zv9va135TtRg9cxwB13N7+9dGJCay9M76qyBCJucZcJ+DUxFBPbeFX62Rh2x1KMIE85Bocr7AYi7tRe7V6l643wsj5OzyB3yGUMRhARERERUdUwM6KOJHfzhf6GDuuvu6PEXNZtYVgzBTr5u+O41giZIOC+aCU6BVTt4ZAavv8M9sfGC0UQxbJghCOt/Nzw77vKOnBEqeR4/XCe3f06+Ff/9h4UroCbAFTWCXTbmGDojSLe+vUGBEHAnN7Va+lJRERERERNG4MRdUStkOH5lkZM7x+Jfx/XY05vP3jerAeQWMfXRnXD10OGv1UzEybI03GmQ4xv9W9vf4UMw5op8MMVg93XW6rkmN3TF1GqsmOvHxlU7XMQERERERExGFHHolRueLe/uq4vgxooVQXLLroGVl4g1Z7Ell52gxHRKjmOjAuFIHA5BhERERER1Q5rRhA1YAEOMiP6hnhAWc3OG7eMaeFpd/vISE8GIoiIiIiIyCkYjCBqwCJvdsso71/9/Gp8TF8PGYZGKGy2j4q0H6QgIiIiIiKqLgYjiBqwcC/bYET3IHd0qWXh04Xllg4FKGQYFGYboCAiIiIiIqoJBiOIGjCFXLDJYni2o0+tl1O09HXDE+3LimkKABb0V1sKrBIREREREdUWC1gSNXDv9VPjib25OK414tFYbyS2VDrluP/qp8YT7b3hr5Ah0NP+chAiIiIiIqKaYDCCqIFr5eeGHfHBAACZkwtMtvar3XIPIiIiIiIiexiMIGoEnB2EICIiIiIiciXWjCAiIiIiIiIiSTEYQURERERERESSYjCCiIiIiIiIiCTFYAQRERERERERSYrBCCIiIiIiIiKSFIMRRERERERERCQpBiOIiIiIiIiISFIMRhARERERERGRpBiMICIiIiIiIiJJMRhBRERERERERJJiMIKIiIiIiIiIJMVgBBERERERERFJisEIIiIiIiIiIpIUgxFEREREREREJCkGI4iIiIiIiIhIUgxGEBEREREREZGkBJ1OJ9b1RRARERERERFR08HMCCIiIiIiIiKSFIMRRERERERERCQpBiOIiIiIiIiISFIMRhARERERERGRpBiMICIiIiIiIiJJMRhRCwsWLEBcXByaN2+OVq1aISkpCSdPnrTaRxRFpKSkoF27dggLC8M999yDU6dOWe0zf/58jB49GhEREVCr1TbnSU9Px+TJk9GxY0eEhYWhV69eWLx4Mcxms0vH11RINY85OTlITExEu3btEBISgo4dO2L69Om4ceOGS8fXVEg1j3fSaDRo37491Go1NBqN08fUFEk5j2q12ubPihUrXDa2pkTq+3H9+vW46667EBoaipiYGDz55JMuGVdTI9U8rlmzxu79qFarceTIEZeOsSmQ8n48cuQIEhIS0KJFC7Ro0QL33nsvfv31V5eNrSmRch737NmDUaNGITIyErGxsXj99ddRWlrqsrE1Jc6Yx0uXLuHZZ59F165dERYWhq5du+LNN99EUVGR1XEuX76MpKQkREREICYmBi+//DJKSkokGWdVMRhRC/v27cPkyZOxfft2bN68GW5ubrjvvvug1Wot+yxevBhLly7FvHnzsGvXLgQHB+P+++9Hfn6+ZR+DwYD4+HhMnTrV7nmOHj2KwMBALFu2DAcOHMDMmTPx7rvvYuHChS4fY1Mg1TzKZDLEx8dj3bp1OHz4MD744APs2bMHL7zwgsvH2BRINY93evrpp9G5c2eXjKepknoelyxZgjNnzlj+TJgwwWVja0qknMdly5Zh9uzZeO65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\n"
          },
          "metadata": {}
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "#Create a new dataframe with only the 'Close Column'\n",
        "data = df.filter(['Close'])\n",
        "#Conver the dataframe to a numpy array\n",
        "dataset = data.values\n",
        "#Get the  number of rows to train the model on\n",
        "training_data_len = math.ceil(len(dataset)*0.8)\n",
        "\n",
        "training_data_len"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "uURw-4M83zgk",
        "outputId": "922a25fb-6aa3-40d2-8c67-50df11edd587"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "1610"
            ]
          },
          "metadata": {},
          "execution_count": 8
        }
      ]
    },
    {
      "cell_type": "markdown",
      "source": [],
      "metadata": {
        "id": "VBBih_8C5i3B"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "#It is always important to SCALE THE DATA\n",
        "#Scaling the data makes it easier to present in RNN\n",
        "scaler = MinMaxScaler(feature_range=(0,1))\n",
        "scaled_data = scaler.fit_transform(dataset)\n",
        "\n",
        "scaled_data"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "EkCM6csc43p2",
        "outputId": "9de7d178-b2f7-49fb-b472-a51b3d560187"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "array([[0.01243228],\n",
              "       [0.01375958],\n",
              "       [0.01651631],\n",
              "       ...,\n",
              "       [0.98381398],\n",
              "       [0.99104513],\n",
              "       [1.        ]])"
            ]
          },
          "metadata": {},
          "execution_count": 9
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "#Create the training dataset\n",
        "#Create the scaled training data\n",
        "train_data = scaled_data[0:training_data_len, :]\n",
        "#Split the data into x_train & y_train\n",
        "x_train = []\n",
        "y_train = []\n",
        "for i in range(60, len(train_data)):\n",
        "  x_train.append(train_data[i-60:i,0])\n",
        "  y_train.append(train_data[i,0])\n",
        "  if i<=60:\n",
        "    print(x_train)\n",
        "    print(y_train)\n",
        "    print()"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "JkEXazmS5q1p",
        "outputId": "e4785c1c-fb2f-494d-fad3-85d1c1113ef1"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "[array([0.01243228, 0.01375958, 0.01651631, 0.01914091, 0.01873851,\n",
            "       0.0196454 , 0.01923099, 0.0185343 , 0.01758536, 0.02052227,\n",
            "       0.02317089, 0.02235408, 0.01787965, 0.02214988, 0.01794572,\n",
            "       0.0337113 , 0.03249211, 0.03408368, 0.03752507, 0.03960912,\n",
            "       0.03943495, 0.03879233, 0.04153103, 0.04410756, 0.04702647,\n",
            "       0.05174113, 0.06164491, 0.06179505, 0.06730851, 0.07142856,\n",
            "       0.06434759, 0.06707427, 0.06702022, 0.07466578, 0.07357869,\n",
            "       0.07559067, 0.07920624, 0.08121825, 0.08701398, 0.09123612,\n",
            "       0.09245533, 0.09288177, 0.08566265, 0.0839209 , 0.08417917,\n",
            "       0.09096589, 0.09287577, 0.09697783, 0.10664737, 0.11954812,\n",
            "       0.11713373, 0.11713972, 0.12646695, 0.12938586, 0.12730777,\n",
            "       0.12540992, 0.12343396, 0.12999843, 0.1345029 , 0.13638876])]\n",
            "[0.13172814323221588]\n",
            "\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "#Let's convert the x_train & Y-train into numpy arrays\n",
        "x_train, y_train = np.array(x_train), np.array(y_train)\n",
        "x_train.shape"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "gGlvokTf9FFI",
        "outputId": "f36d50fb-3f06-4f95-ae13-fa823fc8b006"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "(1550, 60)"
            ]
          },
          "metadata": {},
          "execution_count": 11
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "#Reshape the data\n",
        "#A LSTM network expects the data to be 3 dimensional, i.e.,\n",
        "#1: number of samples\n",
        "#2: number of time steps\n",
        "#3: number of features\n",
        "#IMP from python POV\n",
        "x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))\n",
        "x_train.shape"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "bA6FR3TY-_eR",
        "outputId": "f31cb84e-e409-4170-f363-785df92e42e5"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "(1550, 60, 1)"
            ]
          },
          "metadata": {},
          "execution_count": 12
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "#Build an LSTM Model that contains Layers\n",
        "#Creating layers can provide better security\n",
        "model = Sequential()\n",
        "model.add(LSTM(50, return_sequences= True, input_shape = (x_train.shape[1], 1)))\n",
        "model.add(LSTM(50, return_sequences= False))\n",
        "model.add(Dense(25))\n",
        "model.add(Dense(1))"
      ],
      "metadata": {
        "id": "FoZJuSp2ApBN"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "#Compile the Model\n",
        "model.compile(optimizer = 'adam', loss='mean_squared_error')\n",
        "\n",
        "#Train the current model\n",
        "model.fit(x_train, y_train, batch_size=1, epochs=1)"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "WDsUyDI3EVE7",
        "outputId": "aea4e4cb-ba28-44c5-84fd-1b49880987db"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "1550/1550 [==============================] - 58s 35ms/step - loss: 6.2082e-04\n"
          ]
        },
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "<keras.callbacks.History at 0x7f994a468e50>"
            ]
          },
          "metadata": {},
          "execution_count": 14
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "#Create the testig dataset\n",
        "#Create a new array containing scaled values\n",
        "test_data = scaled_data[training_data_len - 60: , :]\n",
        "#Create X and Y test data set\n",
        "x_test = []\n",
        "y_test = dataset[training_data_len:, :]\n",
        "\n",
        "for i in range(60, len(test_data)):\n",
        "  x_test.append(test_data[i-60:i, 0])"
      ],
      "metadata": {
        "id": "YuRI8pqMLwsD"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "#Conver the Data into a numpy array\n",
        "x_test = np.array(x_test)"
      ],
      "metadata": {
        "id": "mdHaqP43Mkox"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "#Again reshape the data set for LSTM\n",
        "x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))"
      ],
      "metadata": {
        "id": "QUFmWLLNMvch"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "#Get the predicted price value for x test dataset\n",
        "predictions = model.predict(x_test)\n",
        "predictions = scaler.inverse_transform(predictions)"
      ],
      "metadata": {
        "id": "gQRIx5oRNF9S"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "#Get the RMSE for accuracy and efficiency\n",
        "#also the low value of RSME gives the good fit yeilds\n",
        "rmse = np.sqrt(np.mean(predictions - y_test)**2)\n",
        "rmse"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "Z1HcGasUNiBk",
        "outputId": "779bec97-1736-4d0a-b32a-2513ef4bd186"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "1.2273007577924586"
            ]
          },
          "metadata": {},
          "execution_count": 19
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "from IPython.core.pylabtools import figsize\n",
        "#Plot the data\n",
        "train = data[:training_data_len]\n",
        "valid = data[training_data_len:]\n",
        "valid['Predictions'] = predictions\n",
        "\n",
        "#Visualization\n",
        "plt.figure(figsize=(16,8))\n",
        "plt.title('Model')\n",
        "plt.xlabel('Date', fontsize=18)\n",
        "plt.ylabel('Close Price USD ($)', fontsize=18)\n",
        "plt.plot(train['Close'])\n",
        "plt.plot(valid[['Close', 'Predictions']])\n",
        "plt.legend(['Train', 'Val', 'Predictions'], loc = 'lower right')\n",
        "plt.show()"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 662
        },
        "id": "HeRINBwkOHr_",
        "outputId": "eab594b2-0c46-4c71-8145-4c04ab075edc"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stderr",
          "text": [
            "/usr/local/lib/python3.7/dist-packages/ipykernel_launcher.py:5: SettingWithCopyWarning: \n",
            "A value is trying to be set on a copy of a slice from a DataFrame.\n",
            "Try using .loc[row_indexer,col_indexer] = value instead\n",
            "\n",
            "See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy\n",
            "  \"\"\"\n"
          ]
        },
        {
          "output_type": "display_data",
          "data": {
            "text/plain": [
              "<Figure size 1152x576 with 1 Axes>"
            ],
            "image/png": "iVBORw0KGgoAAAANSUhEUgAABCMAAAIdCAYAAAAH77cvAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAALEgAACxIB0t1+/AAAADh0RVh0U29mdHdhcmUAbWF0cGxvdGxpYiB2ZXJzaW9uMy4yLjIsIGh0dHA6Ly9tYXRwbG90bGliLm9yZy+WH4yJAAAgAElEQVR4nOzdd5hdZb33/8+91q7TUieTnhBSSIAEkkAghBAiCCSidAUeiQgiRH0McjgKetTjOf6ojz6ICCJG6aEcQEJAHiQQOlKkhpJeyWRSppdd1vr9MWRm1t57anab4f26Li5n3evea31nVvxjffZdTGVlpSsAAAAAAIAssXJdAAAAAAAA+GIhjAAAAAAAAFlFGAEAAAAAALKKMAIAAAAAAGQVYQQAAAAAAMgqwggAAAAAAJBVhBEAAKBX2bRpk/r376/LLrssL64DAAC6jzACAAB0qH///urfv78GDBigDRs2tNvvtNNOa+m7dOnSLFYIAAB6G8IIAADQKZ/PJ9d1ddddd6U8v3HjRq1atUo+ny/LlQEAgN6IMAIAAHRq4MCBOuKII3TfffcpFoslnb/77rvluq5OPvnkHFQHAAB6G8IIAADQJRdccIHKy8v11FNPedpjsZjuvfdezZgxQwcffHC7n9+4caMWL16sKVOmqLS0VBMmTNC3vvUtffDBByn719TU6Oqrr9aUKVNUVlamI444Qr///e/lum6792hsbNTNN9+s4447TiNGjNDw4cM1b948LV26tMPPAQCA7CKMAAAAXXLGGWeouLg4aarG008/rR07dmjRokXtfvadd97Rcccdp/vvv1+HHnqofvCDH2jOnDl64okndMIJJ2jlypWe/k1NTfra176mP/zhD+rfv78uvfRSzZkzRzfeeKOuuuqqlPeoqanRwoUL9R//8R9yXVfnnXeezj//fFVXV+tHP/qRFi9evP9/BAAAkBZM7AQAAF1SWFios846S3feeae2bNmiUaNGSZLuuusuFRUV6YwzztDNN9+c9DnXdXXppZeqqqpKf/jDH3Teeee1nHv++ed1+umn65JLLtF7772ngoICSdLvf/97vf3221qwYIHuueceWVbz9yeXX3655s2bl7K+q6++Wm+99ZZ++ctfasmSJS3tTU1N+uY3v6n7779fX/3qV3XKKaek608CAAB6iJER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RWHo0KFs7WkjjprHvXv34p133sG1a9eg1+tRv359TJgwAZMnTza7u0Bl58jPY3p6Ot58801s27YNBoMBnTt3xvvvv48GDRrY4cxqF0f/XB00aBCUSiV++OEHG59J7ebIedy/fz8WL16M8+fPQxAEtGzZEm+99VaFM9fIsfM4dOhQnDp1Cnl5eWjRogVmz56Nfv362eGsah9bzOPGjRut1oc4deoU6tWrB6Ag8DRz5kwcOnQIcrkcY8aMwbvvvlulbrowGEFEREREREREDsUFeURERERERETkUAxGEBEREREREZFDMRhBRERERERERA7FYAQRERERERERORSDEURERERERETkUAxGEBEREREREZFDMRhBRERERERERA7FYAQRERFVWFRUFNRqtfGfh4cH6tWrhy5duuCll17C3r17YTAYyn3806dPIyIiAnFxcTYcNREREVUWSWUPgIiIiGqO0aNHo1+/fjAYDMjIyEBsbCx27tyJ7777Dr169cK6deugVqvLfNwzZ85g8eLFePzxx1GvXj07jJyIiIgcicEIIiIispnWrVsjPDzcZNt7772HBQsWYNWqVXjhhRfw448/VtLoiIiIqKrgMg0iIiKyK7FYjEWLFqFLly7Yu3cvoqOjAQB3797Fm2++acx28PX1RadOnfDxxx9Dp9MZnx8REYFXXnkFADB06FDjUpCpU6ca98nNzcVHH32Ezp07w9fXF3Xr1kV4eDhOnTrl2JMlIiKiUmFmBBERETnE+PHjER0djd9++w1dunTBuXPnsH37dgwZMgQNGjSAVqvF77//jv/85z+4fv06Pv74YwAFAYj4+HisW7cOM2bMQKNGjQAADRo0AABotVo8+eST+OuvvxAeHo7JkycjLS0N69evxxNPPIFffvkFbdu2rbTzJiIiInMMRhAREZFDNG/eHABw+fJlAEC3bt1w6tQpCIJg3Ofll1/Giy++iK+//hpz5syBn58fWrRogQ4dOmDdunXo1asXunfvbnLcL774AocPH8bmzZvRp08f4/ZJkyaha9eumD9/Pnbu3OmAMyQiIqLS4jINIiIicghXV1cAQHp6OgBAoVAYAxF5eXlISUlBUlIS+vTpA71ejxMnTpTquN9//z0aNWqENm3aICkpyfhPq9WiV69eOHLkCLKzs+1zUkRERFQuzIwgIiIih0hLSwMAqFQqAEB+fj6WLVuG7777DlevXjVr/anRaEp13EuXLiE7OxsNGza0uk9SUhKCgoLKOXIiIiKyNQYjiIiIyCHOnTsHAAgNDQUAzJs3D1988QVGjRqFGTNmwNvbG05OTjh16hTefvtt6PX6Uh3XYDCgWbNmeO+996zu4+XlVfETICIiIpthMIKIiIgcYsOGDQCA/v37AwAiIyPRtWtXrF271mS/q1evmj23cF2JooKDg5GUlIQePXpAJOIKVCIiouqAv7GJiIjIrnQ6HebPn4/o6Gj0798fnTt3BlDQ8rPo0ozMzEx8+umnZsdQKpUAgJSUFLPHxo0bh/j4eKxatcri6yckJFT0FIiIiMjGmBlBRERENnPq1ClERkYCADIyMhAbG4udO3fi5s2b6N27N7788kvjvsOHD8dXX32FiRMnolevXkhISMCGDRvg4eFhdtx27dpBJBLho48+gkajgVKpRL169fDYY4/hpZdewv79+/HWW2/h0KFD6NGjB1QqFW7duoWDBw9CJpNhx44dDvseEBERUckEjUZjKHk3IiIiIuuioqIwdOhQ49cikQguLi4ICAhAmzZtMHr0aPTt29fkOVlZWYiIiMDWrVuRmJiIwMBATJgwAe3atcPw4cOxatUqPPPMM8b9N23ahOXLl+Pq1avQarUYN24cPvvsMwAFxTDXrFmDyMhIxMTEAAD8/PzQvn17jBs3Dr1793bAd4GIiIhKi8EIIiIiIiIiInIo1owgIiIiIiIiIodiMIKIiIiIiIiIHIrBCCIiIiIiIiJyKAYjiIiIiIiIiMihGIwgIiIiIiIiIodiMIKIiIiIiIiIHIrBCCIiIiIiIiJyKAYjiIiIiIiIiMihGIwgIiIiIiIiIodiMIKIiIiIiIiIHOr/AWlj8jlV36WmAAAAAElFTkSuQmCC\n"
          },
          "metadata": {}
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "valid"
      ],
      "metadata": {
        "id": "IBf2hmZqAdqc",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 455
        },
        "outputId": "a90c8cbd-0927-4c86-f4a7-199cba9f70b1"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "                Close  Predictions\n",
              "Date                              \n",
              "2018-05-29  46.974998    46.231888\n",
              "2018-05-30  46.875000    46.265171\n",
              "2018-05-31  46.717499    46.271355\n",
              "2018-06-01  47.560001    46.244431\n",
              "2018-06-04  47.957500    46.325809\n",
              "...               ...          ...\n",
              "2019-12-24  71.067497    66.990601\n",
              "2019-12-26  72.477501    67.252457\n",
              "2019-12-27  72.449997    67.671524\n",
              "2019-12-30  72.879997    68.068726\n",
              "2019-12-31  73.412498    68.459549\n",
              "\n",
              "[402 rows x 2 columns]"
            ],
            "text/html": [
              "\n",
              "  <div id=\"df-19881cfc-4900-43a2-aabb-e4e009ae46f5\">\n",
              "    <div class=\"colab-df-container\">\n",
              "      <div>\n",
              "<style scoped>\n",
              "    .dataframe tbody tr th:only-of-type {\n",
              "        vertical-align: middle;\n",
              "    }\n",
              "\n",
              "    .dataframe tbody tr th {\n",
              "        vertical-align: top;\n",
              "    }\n",
              "\n",
              "    .dataframe thead th {\n",
              "        text-align: right;\n",
              "    }\n",
              "</style>\n",
              "<table border=\"1\" class=\"dataframe\">\n",
              "  <thead>\n",
              "    <tr style=\"text-align: right;\">\n",
              "      <th></th>\n",
              "      <th>Close</th>\n",
              "      <th>Predictions</th>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>Date</th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "    </tr>\n",
              "  </thead>\n",
              "  <tbody>\n",
              "    <tr>\n",
              "      <th>2018-05-29</th>\n",
              "      <td>46.974998</td>\n",
              "      <td>46.231888</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>2018-05-30</th>\n",
              "      <td>46.875000</td>\n",
              "      <td>46.265171</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>2018-05-31</th>\n",
              "      <td>46.717499</td>\n",
              "      <td>46.271355</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>2018-06-01</th>\n",
              "      <td>47.560001</td>\n",
              "      <td>46.244431</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>2018-06-04</th>\n",
              "      <td>47.957500</td>\n",
              "      <td>46.325809</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>...</th>\n",
              "      <td>...</td>\n",
              "      <td>...</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>2019-12-24</th>\n",
              "      <td>71.067497</td>\n",
              "      <td>66.990601</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>2019-12-26</th>\n",
              "      <td>72.477501</td>\n",
              "      <td>67.252457</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>2019-12-27</th>\n",
              "      <td>72.449997</td>\n",
              "      <td>67.671524</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>2019-12-30</th>\n",
              "      <td>72.879997</td>\n",
              "      <td>68.068726</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>2019-12-31</th>\n",
              "      <td>73.412498</td>\n",
              "      <td>68.459549</td>\n",
              "    </tr>\n",
              "  </tbody>\n",
              "</table>\n",
              "<p>402 rows × 2 columns</p>\n",
              "</div>\n",
              "      <button class=\"colab-df-convert\" onclick=\"convertToInteractive('df-19881cfc-4900-43a2-aabb-e4e009ae46f5')\"\n",
              "              title=\"Convert this dataframe to an interactive table.\"\n",
              "              style=\"display:none;\">\n",
              "        \n",
              "  <svg xmlns=\"http://www.w3.org/2000/svg\" height=\"24px\"viewBox=\"0 0 24 24\"\n",
              "       width=\"24px\">\n",
              "    <path d=\"M0 0h24v24H0V0z\" fill=\"none\"/>\n",
              "    <path d=\"M18.56 5.44l.94 2.06.94-2.06 2.06-.94-2.06-.94-.94-2.06-.94 2.06-2.06.94zm-11 1L8.5 8.5l.94-2.06 2.06-.94-2.06-.94L8.5 2.5l-.94 2.06-2.06.94zm10 10l.94 2.06.94-2.06 2.06-.94-2.06-.94-.94-2.06-.94 2.06-2.06.94z\"/><path d=\"M17.41 7.96l-1.37-1.37c-.4-.4-.92-.59-1.43-.59-.52 0-1.04.2-1.43.59L10.3 9.45l-7.72 7.72c-.78.78-.78 2.05 0 2.83L4 21.41c.39.39.9.59 1.41.59.51 0 1.02-.2 1.41-.59l7.78-7.78 2.81-2.81c.8-.78.8-2.07 0-2.86zM5.41 20L4 18.59l7.72-7.72 1.47 1.35L5.41 20z\"/>\n",
              "  </svg>\n",
              "      </button>\n",
              "      \n",
              "  <style>\n",
              "    .colab-df-container {\n",
              "      display:flex;\n",
              "      flex-wrap:wrap;\n",
              "      gap: 12px;\n",
              "    }\n",
              "\n",
              "    .colab-df-convert {\n",
              "      background-color: #E8F0FE;\n",
              "      border: none;\n",
              "      border-radius: 50%;\n",
              "      cursor: pointer;\n",
              "      display: none;\n",
              "      fill: #1967D2;\n",
              "      height: 32px;\n",
              "      padding: 0 0 0 0;\n",
              "      width: 32px;\n",
              "    }\n",
              "\n",
              "    .colab-df-convert:hover {\n",
              "      background-color: #E2EBFA;\n",
              "      box-shadow: 0px 1px 2px rgba(60, 64, 67, 0.3), 0px 1px 3px 1px rgba(60, 64, 67, 0.15);\n",
              "      fill: #174EA6;\n",
              "    }\n",
              "\n",
              "    [theme=dark] .colab-df-convert {\n",
              "      background-color: #3B4455;\n",
              "      fill: #D2E3FC;\n",
              "    }\n",
              "\n",
              "    [theme=dark] .colab-df-convert:hover {\n",
              "      background-color: #434B5C;\n",
              "      box-shadow: 0px 1px 3px 1px rgba(0, 0, 0, 0.15);\n",
              "      filter: drop-shadow(0px 1px 2px rgba(0, 0, 0, 0.3));\n",
              "      fill: #FFFFFF;\n",
              "    }\n",
              "  </style>\n",
              "\n",
              "      <script>\n",
              "        const buttonEl =\n",
              "          document.querySelector('#df-19881cfc-4900-43a2-aabb-e4e009ae46f5 button.colab-df-convert');\n",
              "        buttonEl.style.display =\n",
              "          google.colab.kernel.accessAllowed ? 'block' : 'none';\n",
              "\n",
              "        async function convertToInteractive(key) {\n",
              "          const element = document.querySelector('#df-19881cfc-4900-43a2-aabb-e4e009ae46f5');\n",
              "          const dataTable =\n",
              "            await google.colab.kernel.invokeFunction('convertToInteractive',\n",
              "                                                     [key], {});\n",
              "          if (!dataTable) return;\n",
              "\n",
              "          const docLinkHtml = 'Like what you see? Visit the ' +\n",
              "            '<a target=\"_blank\" href=https://colab.research.google.com/notebooks/data_table.ipynb>data table notebook</a>'\n",
              "            + ' to learn more about interactive tables.';\n",
              "          element.innerHTML = '';\n",
              "          dataTable['output_type'] = 'display_data';\n",
              "          await google.colab.output.renderOutput(dataTable, element);\n",
              "          const docLink = document.createElement('div');\n",
              "          docLink.innerHTML = docLinkHtml;\n",
              "          element.appendChild(docLink);\n",
              "        }\n",
              "      </script>\n",
              "    </div>\n",
              "  </div>\n",
              "  "
            ]
          },
          "metadata": {},
          "execution_count": 21
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "apple_quote = web.DataReader('AAPL', data_source='yahoo', start='2012-01-01', end='2019-12-31')\n",
        "#Create a new dataframe\n",
        "new_df = apple_quote.filter(['Close'])\n",
        "#Get the last 60 days of data\n",
        "last_60_days = new_df[-60:].values\n",
        "#Scale the data to be values between 0 and 1\n",
        "last_60_days_scaled = scaler.transform(last_60_days)\n",
        "#Create an empty list\n",
        "X_test = []\n",
        "#Append the past 60 days data\n",
        "X_test.append(last_60_days_scaled)\n",
        "#Convert the X-test data set into numpy array\n",
        "X_test = np.array(X_test)\n",
        "#Reshape for LSTM\n",
        "X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))\n",
        "#Define predicted price\n",
        "pred_price = model.predict(X_test)\n",
        "#Get the predicted scaled price\n",
        "pred_price = scaler.inverse_transform(pred_price)\n",
        "print(pred_price)"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "R9OhsQ3jN8-m",
        "outputId": "268164a2-9c93-4316-b88e-ea8c75f7035e"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "[[68.8572]]\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "# Final Predictions\n",
        "apple_quote2 = web.DataReader('AAPL', data_source='yahoo', start='2019-12-30', end='2019-12-31')\n",
        "print(apple_quote2['Close'])"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "iaelOWHUP-OL",
        "outputId": "4853eddf-e3ec-4da2-9a81-2e18419c03fd"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Date\n",
            "2019-12-30    72.879997\n",
            "2019-12-31    73.412498\n",
            "Name: Close, dtype: float64\n"
          ]
        }
      ]
    }
  ]
}
