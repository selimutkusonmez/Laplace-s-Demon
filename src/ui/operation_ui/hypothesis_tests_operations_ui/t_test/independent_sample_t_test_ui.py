        html_formul = f"""
            <table align="center" cellpadding="0" cellspacing="0" >
                <tr>
                    <td valign="middle" style="padding-right: 15px; font-style: italic;">
                        t = 
                    </td>
                    
                    <td valign="middle">
                        <table cellpadding="0" cellspacing="0">
                            <tr>
                                <td align="center" style="border-bottom: 2px solid currentColor; padding: 0 10px 6px 10px;">
                                    {self.variable_1_display} &minus; {self.variable_4_display}
                                </td>
                            </tr>
                            <tr>
                                <td align="center" style="padding: 8px 10px 0 10px;">
                                    
                                    <table cellpadding="0" cellspacing="0" align="center">
                                        <tr>
                                            <td valign="center" style="font-size: 80px;line-height: 0.8;">
                                                &radic;
                                            </td>
                                            <td valign="middle" style="border-top: 2px solid #ADBAC7; padding-top: 6px; width: 200px;">
                                                
                                                <table cellpadding="0" cellspacing="0" align="center">
                                                    <tr>
                                                        <td align="center">
                                                            <table cellpadding="0" cellspacing="0">
                                                                <tr><td align="center" style="border-bottom: 1px solid currentColor; padding: 0 6px 2px 6px; font-size: 30px;">{self.variable_3_display}</td></tr>
                                                                <tr><td align="center" style="padding: 2px 6px 0 6px; font-size: 30px;">{self.variable_2_display}</td></tr>
                                                            </table>
                                                        </td>
                                                        
                                                        <td valign="middle" style="padding: 0 10px;">
                                                        +
                                                        </td>
                                                        
                                                        <td align="center">
                                                            <table cellpadding="0" cellspacing="0">
                                                                <tr><td align="center" style="border-bottom: 1px solid currentColor; padding: 0 6px 2px 6px; font-size: 30px;">{self.variable_6_display}</td></tr>
                                                                <tr><td align="center" style="padding: 2px 6px 0 6px; font-size: 30px;">{self.variable_5_display}</td></tr>
                                                            </table>
                                                        </td>
                                                    </tr>
                                                </table>

                                            </td>
                                        </tr>
                                    </table>

                                </td>
                            </tr>
                        </table>
                    </td>

                    <td valign="middle" style="padding-left: 20px;">
                        = {self.current_result}
                    </td>
                </tr>
            </table>
        """
        self.dynamic_formula.setText(html_formul)
