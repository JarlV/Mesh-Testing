#include "nrf_drv_common.h"
#include "nrf_drv_ppi.h"
#include "nrf_drv_gpiote.h"
#include <nrf.h>

uint32_t err_code;
typedef uint32_t ret_code_t;
nrf_ppi_channel_t ppi_channel5;

// set ppi for end event and led 1 toggle
void set_ppi(int pin, uint32_t event, nrf_ppi_channel_t ppi_channel){
    ret_code_t c = nrf_drv_gpiote_init();
    
    //config event task
    nrf_drv_gpiote_out_config_t config = GPIOTE_CONFIG_OUT_TASK_TOGGLE(true);
    
    //config event task for radio
    err_code = nrf_drv_gpiote_out_init(pin, &config);
		
		err_code = nrf_drv_ppi_channel_alloc(&ppi_channel);
    APP_ERROR_CHECK(err_code);
    err_code = nrf_drv_ppi_channel_assign(ppi_channel,
										event,
										nrf_drv_gpiote_out_task_addr_get(pin));
    err_code = nrf_drv_ppi_channel_enable(ppi_channel);
		nrf_drv_gpiote_out_task_enable(pin);
}

void gpiote_out_init(uint32_t index, uint32_t pin, uint32_t polarity, uint32_t init_val) {
    NRF_GPIOTE->CONFIG[index] |= ((GPIOTE_CONFIG_MODE_Task << GPIOTE_CONFIG_MODE_Pos) & GPIOTE_CONFIG_MODE_Msk) |
                            ((pin << GPIOTE_CONFIG_PSEL_Pos) & GPIOTE_CONFIG_PSEL_Msk) |
                            ((polarity << GPIOTE_CONFIG_POLARITY_Pos) & GPIOTE_CONFIG_POLARITY_Msk) |
                            ((init_val << GPIOTE_CONFIG_OUTINIT_Pos) & GPIOTE_CONFIG_OUTINIT_Msk);
}

void init_ppi() {
    const uint32_t GPIO_CH = 0;
    const uint32_t PPI_CH0 = 10;
    const uint32_t PPI_CH1 = 11;
    gpiote_out_init(GPIO_CH, 20, GPIOTE_CONFIG_POLARITY_Toggle, GPIOTE_CONFIG_OUTINIT_Low);

    NRF_PPI->CH[PPI_CH0].EEP = (uint32_t) &(NRF_RADIO->EVENTS_READY);
    NRF_PPI->CH[PPI_CH0].TEP = (uint32_t) &(NRF_GPIOTE->TASKS_OUT[GPIO_CH]);
    NRF_PPI->CH[PPI_CH1].EEP = (uint32_t) &(NRF_RADIO->EVENTS_END);
    NRF_PPI->CH[PPI_CH1].TEP = (uint32_t) &(NRF_GPIOTE->TASKS_OUT[GPIO_CH]);
    NRF_PPI->CHENSET = (1 << PPI_CH0) | (1 << PPI_CH1);
}

int main(void){
	set_ppi(24, 			// LED 4
			0x40001108, 	// payload
			ppi_channel5);
}